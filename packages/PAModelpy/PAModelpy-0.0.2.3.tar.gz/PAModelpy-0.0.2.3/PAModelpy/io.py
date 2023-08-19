#from GECKOpy: https://geckopy.readthedocs.io/en/latest/_modules/geckopy/io.html#write_sbml_ec_model
from .PAModel import PAModel
import datetime
from .CatalyticEvent import Constant
from .EnzymeSectors import ActiveEnzymeSector
from typing import Optional
import logging
from collections import defaultdict
import numbers
import re

import libsbml
from cobra import Configuration
from cobra.core.gene import parse_gpr
from cobra.io.sbml import (
    BOUND_MINUS_INF,
    BOUND_PLUS_INF,
    F_GENE,
    F_GENE_REV,
    F_GROUP,
    F_GROUP_REV,
    F_REACTION,
    F_REACTION_REV,
    F_REPLACE,
    F_SPECIE,
    F_SPECIE_REV,
    LONG_SHORT_DIRECTION,
    LOWER_BOUND_ID,
    SBO_DEFAULT_FLUX_BOUND,
    SBO_EXCHANGE_REACTION,
    SBO_FBA_FRAMEWORK,
    SBO_FLUX_BOUND,
    SHORT_LONG_DIRECTION,
    UNITS_FLUX,
    UPPER_BOUND_ID,
    ZERO_BOUND_ID,
    CobraSBMLError,
    Gene,
    Group,
    Metabolite,
    _check,
    _check_required,
    _create_bound,
    _create_parameter,
    _get_doc_from_filename,
    _parse_annotations,
    _parse_notes_dict,
    _sbase_annotations,
    _sbase_notes_dict,
    linear_reaction_coefficients,
)
from cobra.util.solver import set_objective

from .PAModel import PAModel
from .Enzyme import Enzyme
from .CatalyticEvent import CatalyticEvent, Constant
from cobra.core import Reaction, Metabolite
from pathlib import Path

__all__ = ["read_sbml_pamodel", "write_sbml_pamodel"]

LOGGER = logging.getLogger(__name__)
config = Configuration()
PROT_PATTERN = re.compile(
    r"EC_*"
)
CE_PATTERN = re.compile(
    r"CE_*"
)

config = Configuration()

def read_sbml_pamodel(
    filename: str,
    number: float = float,
    # re.Pattern does not exist in py36 so this type hint cannot be added now
    f_replace=F_REPLACE,
    set_missing_bounds: bool = False,
    hardcoded_rev_reactions: bool = True,
    **kwargs,
) -> PAModel:
    """Create `PAModelpy.PAModel` from SBMLDocument.

    Parameters
    ----------
    filename: str
    number: data type of stoichiometry: {float, int}
        In which data type should the stoichiometry be parsed.
    f_replace : dict of replacement functions for id replacement
    set_missing_bounds : flag to set missing bounds
    hardcoded_rev_reactions: bool
        if reversible reaction to account for proteins being consumed on both
        directions are written explicitly for in the SBML

    Returns
    -------
    cobra.core.Model

    """
    try:
        fsanitized = str(filename) if isinstance(filename, Path) else filename
        doc = _get_doc_from_filename(fsanitized)
    except IOError as e:
        raise e
    except Exception as original_error:
        raise CobraSBMLError(
            "Something went wrong reading the SBML model. Most likely the SBML"
            " model is not valid. Please check that your model is valid using "
            "the `cobra.io.sbml.validate_sbml_model` function or via the "
            "online validator at http://sbml.org/validator .\n"
            "\t`(model, errors) = validate_sbml_model(filename)`"
            "\nIf the model is valid and cannot be read please open an issue "
            f"at https://github.com/opencobra/cobrapy/issues: {original_error}"
        )

    if f_replace is None:
        f_replace = {}

    # SBML model
    model: libsbml.Model = doc.getModel()
    if model is None:
        raise CobraSBMLError("No SBML model detected in file.")
    model_fbc: libsbml.FbcModelPlugin = model.getPlugin("fbc")

    if not model_fbc:
        LOGGER.warning("Model does not contain SBML fbc package information.")
    else:
        if not model_fbc.isSetStrict():
            LOGGER.warning('Loading SBML model without fbc:strict="true"')

        # fbc-v1 (legacy)
        doc_fbc = doc.getPlugin("fbc")  # type: libsbml.FbcSBMLDocumentPlugin
        fbc_version = doc_fbc.getPackageVersion()

        if fbc_version == 1:
            LOGGER.warning(
                "Loading SBML with fbc-v1 (models should be encoded" " using fbc-v2)"
            )
            conversion_properties = libsbml.ConversionProperties()
            conversion_properties.addOption(
                "convert fbc v1 to fbc v2", True, "Convert FBC-v1 model to FBC-v2"
            )
            result = doc.convert(conversion_properties)
            if result != libsbml.LIBSBML_OPERATION_SUCCESS:
                raise Exception("Conversion of SBML fbc v1 to fbc v2 failed")

    # Model
    model_id = model.getIdAttribute()
    if not libsbml.SyntaxChecker.isValidSBMLSId(model_id):
        LOGGER.error("'%s' is not a valid SBML 'SId'." % model_id)
    pamodel = PAModel(model_id)
    pamodel.name = model.getName()

    # meta information
    meta = {
        "model.id": model_id,
        "level": model.getLevel(),
        "version": model.getVersion(),
        "packages": [],
    }
    # History
    creators = []
    created = None
    if model.isSetModelHistory():
        history = model.getModelHistory()  # type: libsbml.ModelHistory

        if history.isSetCreatedDate():
            created = history.getCreatedDate()

        for c in history.getListCreators():  # type: libsbml.ModelCreator
            creators.append(
                {
                    "familyName": c.getFamilyName() if c.isSetFamilyName() else None,
                    "givenName": c.getGivenName() if c.isSetGivenName() else None,
                    "organisation": c.getOrganisation()
                    if c.isSetOrganisation()
                    else None,
                    "email": c.getEmail() if c.isSetEmail() else None,
                }
            )

    meta["creators"] = creators
    meta["created"] = created
    meta["notes"] = _parse_notes_dict(doc)
    meta["annotation"] = _parse_annotations(doc)

    info = "<{}> SBML L{}V{}".format(model_id, model.getLevel(), model.getVersion())
    packages = {}
    for k in range(doc.getNumPlugins()):
        plugin = doc.getPlugin(k)  # type:libsbml.SBasePlugin
        key, value = plugin.getPackageName(), plugin.getPackageVersion()
        packages[key] = value
        info += ", {}-v{}".format(key, value)
        if key not in ["fbc", "groups", "l3v2extendedmath"]:
            LOGGER.warning(
                "SBML package '%s' not supported by cobrapy, "
                "information is not parsed",
                key,
            )
    meta["info"] = info
    meta["packages"] = packages
    pamodel._sbml = meta

    # notes and annotations
    pamodel.notes = _parse_notes_dict(model)
    pamodel.annotation = _parse_annotations(model)

    # Compartments
    # FIXME: update with new compartments
    compartments = {}
    for (
        compartment
    ) in model.getListOfCompartments():  # noqa: E501 type: libsbml.Compartment
        cid = _check_required(compartment, compartment.getIdAttribute(), "id")
        compartments[cid] = compartment.getName()
    pamodel.compartments = compartments

    # Species
    metabolites = []
    # proteins that rely on the naming convention "prot_UNIPROT_ID" will be
    # catched here. Those who are annotated by groups membership will be parsed
    # after the groups are processed.
    enzymes = []
    boundary_metabolites = []
    if model.getNumSpecies() == 0:
        LOGGER.warning("No metabolites in model")

    for specie in model.getListOfSpecies():  # type: libsbml.Species
        sid = _check_required(specie, specie.getIdAttribute(), "id")
        if f_replace and F_SPECIE in f_replace:
            sid = f_replace[F_SPECIE](sid)
        if not PROT_PATTERN.match(met.id):
            met = Metabolite(sid)
            met.name = specie.getName()
            met.notes = _parse_notes_dict(specie)
            met.annotation = _parse_annotations(specie)
            met.compartment = specie.getCompartment()
            initial_amount = specie.getInitialAmount()
            metabolites.append(met)

            specie_fbc = specie.getPlugin("fbc")  # type: libsbml.FbcSpeciesPlugin
            if specie_fbc:
                met.charge = specie_fbc.getCharge()
                met.formula = specie_fbc.getChemicalFormula()
            else:
                if specie.isSetCharge():
                    LOGGER.warning(
                    "Use of the species charge attribute is "
                    "discouraged, use fbc:charge "
                    "instead: %s",
                    specie,
                    )
                    met.charge = specie.getCharge()
                else:
                    if "CHARGE" in met.notes:
                        LOGGER.warning(
                        "Use of CHARGE in the notes element is "
                        "discouraged, use fbc:charge "
                        "instead: %s",
                        specie,
                        )
                        try:
                            met.charge = int(met.notes["CHARGE"])
                        except ValueError:
                            # handle nan, na, NA, ...
                            pass

                if "FORMULA" in met.notes:
                    LOGGER.warning(
                        "Use of FORMULA in the notes element is "
                        "discouraged, use fbc:chemicalFormula "
                        "instead: %s",
                        specie,
                    )
                    met.formula = met.notes["FORMULA"]

            # Detect boundary metabolites
            if specie.getBoundaryCondition() is True:
                boundary_metabolites.append(met)
        else:
            enzymes.append(specie)

    pamodel.add_metabolites(metabolites)

    # Add exchange reactions for boundary metabolites
    ex_reactions = []
    for met in boundary_metabolites:
        ex_rid = "EX_{}".format(met.id)
        ex_reaction = Reaction(ex_rid)
        ex_reaction.name = ex_rid
        ex_reaction.annotation = {"sbo": SBO_EXCHANGE_REACTION}
        ex_reaction.lower_bound = config.lower_bound
        ex_reaction.upper_bound = config.upper_bound
        LOGGER.warning(
            "Adding exchange reaction %s with default bounds "
            "for boundary metabolite: %s." % (ex_reaction.id, met.id)
        )
        # species is reactant
        ex_reaction.add_metabolites({met: -1})
        ex_reactions.append(ex_reaction)
    pamodel.add_reactions(ex_reactions)

    # Genes
    if model_fbc:
        for (
            gp
        ) in model_fbc.getListOfGeneProducts():  # noqa: E501 type: libsbml.GeneProduct
            gid = _check_required(gp, gp.getIdAttribute(), "id")
            if f_replace and F_GENE in f_replace:
                gid = f_replace[F_GENE](gid)
            cobra_gene = Gene(gid)
            cobra_gene.name = gp.getName()
            if cobra_gene.name is None:
                cobra_gene.name = gid
            cobra_gene.annotation = _parse_annotations(gp)
            cobra_gene.notes = _parse_notes_dict(gp)

            pamodel.genes.append(cobra_gene)
    else:
        for (
            cobra_reaction
        ) in model.getListOfReactions():  # noqa: E501 type: libsbml.Reaction
            # fallback to notes information
            notes = _parse_notes_dict(cobra_reaction)
            if "GENE ASSOCIATION" in notes:
                gpr = notes["GENE ASSOCIATION"]
            elif "GENE_ASSOCIATION" in notes:
                gpr = notes["GENE_ASSOCIATION"]
            else:
                gpr = ""

            if len(gpr) > 0:
                gpr = gpr.replace("(", ";")
                gpr = gpr.replace(")", ";")
                gpr = gpr.replace("or", ";")
                gpr = gpr.replace("and", ";")
                # Interaction of the above replacements can lead to multiple
                # ;, which results in empty gids
                gids = [t.strip() for t in gpr.split(";")]
                gids = set(gids).difference({""})

                # create missing genes
                for gid in gids:
                    if f_replace and F_GENE in f_replace:
                        gid = f_replace[F_GENE](gid)

                    if gid not in pamodel.genes:
                        cobra_gene = Gene(gid)
                        cobra_gene.name = gid
                        pamodel.genes.append(cobra_gene)

    # GPR rules
    def process_association(ass):
        """Recursively convert gpr association to a gpr string.

        Defined as inline functions to not pass the replacement dict around.
        """
        if ass.isFbcOr():
            return " ".join(
                [
                    "(",
                    " or ".join(
                        process_association(c) for c in ass.getListOfAssociations()
                    ),
                    ")",
                ]
            )
        elif ass.isFbcAnd():
            return " ".join(
                [
                    "(",
                    " and ".join(
                        process_association(c) for c in ass.getListOfAssociations()
                    ),
                    ")",
                ]
            )
        elif ass.isGeneProductRef():
            gid = ass.getGeneProduct()
            if f_replace and F_GENE in f_replace:
                return f_replace[F_GENE](gid)
            else:
                return gid

    # Reactions
    missing_bounds = False
    catalytic_events = []
    reactions = []
    if model.getNumReactions() == 0:
        LOGGER.warning("No reactions in model")

    for reaction in model.getListOfReactions():  # type: libsbml.Reaction
        rid = _check_required(reaction, reaction.getIdAttribute(), "id")
        # proteins are parsed based on Species, prot exchanges are ignored
        if CE_PATTERN.search(rid):
            catalytic_events.append(reaction)
            # parse equation
            stoichiometry = defaultdict(lambda: 0)
            for (sref) in reaction.getListOfReactants():  # noqa: E501 type: libsbml.SpeciesReference
                sid = _check_required(sref, sref.getSpecies(), "species")

                if f_replace and F_SPECIE in f_replace:
                    sid = f_replace[F_SPECIE](sid)
                stoichiometry[sid] -= number(
                    _check_required(sref, sref.getStoichiometry(), "stoichiometry")
                )

            for (sref) in reaction.getListOfProducts():  # noqa: E501 type: libsbml.SpeciesReference
                sid = _check_required(sref, sref.getSpecies(), "species")

                if f_replace and F_SPECIE in f_replace:
                    sid = f_replace[F_SPECIE](sid)
                stoichiometry[sid] += number(
                    _check_required(sref, sref.getStoichiometry(), "stoichiometry")
                )

            # convert to metabolite objects
            object_stoichiometry = {}
            for enz_id in stoichiometry:
                #TODO
                # enz = Enzymes(
                #     id=enz_id,
                #
                #
                # )
                target_set = (
                    pamodel.enzymes
                    if met_id in pamodel.enzymes
                    else pamodel.metabolites
                )
                metabolite = target_set.get_by_id(met_id)
                object_stoichiometry[metabolite] = stoichiometry[met_id]
            cobra_reaction.add_metabolites(object_stoichiometry)

        else:
            if f_replace and F_REACTION in f_replace:
                rid = f_replace[F_REACTION](rid)
            cobra_reaction = Reaction(rid)
            cobra_reaction.name = reaction.getName()
            cobra_reaction.annotation = _parse_annotations(reaction)
            cobra_reaction.notes = _parse_notes_dict(reaction)

        # set bounds
        p_ub, p_lb = None, None
        r_fbc = reaction.getPlugin("fbc")  # type: libsbml.FbcReactionPlugin
        if r_fbc:
            # bounds in fbc
            lb_id = r_fbc.getLowerFluxBound()
            if lb_id:
                p_lb = model.getParameter(lb_id)  # type: libsbml.Parameter
                if p_lb and p_lb.getConstant() and (p_lb.getValue() is not None):
                    cobra_reaction.lower_bound = p_lb.getValue()
                else:
                    raise CobraSBMLError(
                        "No constant bound '%s' for " "reaction: %s" % (p_lb, reaction)
                    )

            ub_id = r_fbc.getUpperFluxBound()
            if ub_id:
                p_ub = model.getParameter(ub_id)  # type: libsbml.Parameter
                if p_ub and p_ub.getConstant() and (p_ub.getValue() is not None):
                    cobra_reaction.upper_bound = p_ub.getValue()
                else:
                    raise CobraSBMLError(
                        "No constant bound '%s' for " "reaction: %s" % (p_ub, reaction)
                    )

            elif reaction.isSetKineticLaw():
                # some legacy models encode bounds in kinetic laws
                klaw = reaction.getKineticLaw()  # type: libsbml.KineticLaw
                p_lb = klaw.getParameter(
                    "LOWER_BOUND"
                )  # noqa: E501 type: libsbml.LocalParameter
                if p_lb:
                    cobra_reaction.lower_bound = p_lb.getValue()
                p_ub = klaw.getParameter(
                    "UPPER_BOUND"
                )  # noqa: E501 type: libsbml.LocalParameter
                if p_ub:
                    cobra_reaction.upper_bound = p_ub.getValue()

                if p_ub is not None or p_lb is not None:
                    LOGGER.warning(
                        "Encoding LOWER_BOUND and UPPER_BOUND in "
                        "KineticLaw is discouraged, "
                        "use fbc:fluxBounds instead: %s",
                        reaction,
                    )

            if p_lb is None:
                missing_bounds = True
                lower_bound = config.lower_bound
                cobra_reaction.lower_bound = lower_bound
                LOGGER.warning(
                    "Missing lower flux bound set to '%s' for " " reaction: '%s'",
                    lower_bound,
                    reaction,
                )

            if p_ub is None:
                missing_bounds = True
                upper_bound = config.upper_bound
                cobra_reaction.upper_bound = upper_bound
                LOGGER.warning(
                    "Missing upper flux bound set to '%s' for " " reaction: '%s'",
                    upper_bound,
                    reaction,
                )

            # add reaction
            reactions.append(cobra_reaction)

            # parse equation
            stoichiometry = defaultdict(lambda: 0)
            for (
                sref
            ) in reaction.getListOfReactants():  # noqa: E501 type: libsbml.SpeciesReference
                sid = _check_required(sref, sref.getSpecies(), "species")

                if f_replace and F_SPECIE in f_replace:
                    sid = f_replace[F_SPECIE](sid)
                stoichiometry[sid] -= number(
                    _check_required(sref, sref.getStoichiometry(), "stoichiometry")
                )

            for (
                sref
            ) in reaction.getListOfProducts():  # noqa: E501 type: libsbml.SpeciesReference
                sid = _check_required(sref, sref.getSpecies(), "species")

                if f_replace and F_SPECIE in f_replace:
                    sid = f_replace[F_SPECIE](sid)
                stoichiometry[sid] += number(
                    _check_required(sref, sref.getStoichiometry(), "stoichiometry")
                )

            # convert to metabolite objects
            object_stoichiometry = {}
            for met_id in stoichiometry:
                target_set = (
                    pamodel.proteins
                    if met_id in pamodel.proteins
                    else pamodel.metabolites
                )
                metabolite = target_set.get_by_id(met_id)
                object_stoichiometry[metabolite] = stoichiometry[met_id]
            cobra_reaction.add_metabolites(object_stoichiometry)

            # GPR
            if r_fbc:
                gpr = ""
                gpa = (
                    r_fbc.getGeneProductAssociation()
                )  # noqa: E501 type: libsbml.GeneProductAssociation
                if gpa is not None:
                    association = (
                        gpa.getAssociation()
                    )  # noqa: E501 type: libsbml.FbcAssociation
                    gpr = process_association(association)
            else:
                # fallback to notes information
                notes = cobra_reaction.notes
                if "GENE ASSOCIATION" in notes:
                    gpr = notes["GENE ASSOCIATION"]
                elif "GENE_ASSOCIATION" in notes:
                    gpr = notes["GENE_ASSOCIATION"]
                else:
                    gpr = ""

                if len(gpr) > 0:
                    LOGGER.warning(
                        "Use of GENE ASSOCIATION or GENE_ASSOCIATION "
                        "in the notes element is discouraged, use "
                        "fbc:gpr instead: %s",
                        reaction,
                    )
                    if f_replace and F_GENE in f_replace:
                        gpr = " ".join(f_replace[F_GENE](t) for t in gpr.split(" "))

            # remove outside parenthesis, if any
            if gpr.startswith("(") and gpr.endswith(")"):
                try:
                    parse_gpr(gpr[1:-1].strip())
                    gpr = gpr[1:-1].strip()
                except (SyntaxError, TypeError) as e:
                    LOGGER.warning(
                        f"Removing parenthesis from gpr {gpr} leads to "
                        f"an error, so keeping parenthesis, error: {e}",
                    )

            cobra_reaction.gene_reaction_rule = gpr

    pamodel.add_reactions(reactions)

    # Objective
    obj_direction = "max"
    coefficients = {}
    if model_fbc:
        obj_list = (
            model_fbc.getListOfObjectives()
        )  # noqa: E501 type: libsbml.ListOfObjectives
        if obj_list is None:
            LOGGER.warning("listOfObjectives element not found")
        elif obj_list.size() == 0:
            LOGGER.warning("No objective in listOfObjectives")
        elif not obj_list.getActiveObjective():
            LOGGER.warning("No active objective in listOfObjectives")
        else:
            obj_id = obj_list.getActiveObjective()
            obj = model_fbc.getObjective(obj_id)  # type: libsbml.Objective
            obj_direction = LONG_SHORT_DIRECTION[obj.getType()]

            for (
                flux_obj
            ) in (
                obj.getListOfFluxObjectives()
            ):  # noqa: E501 type: libsbml.FluxObjective
                rid = flux_obj.getReaction()
                if f_replace and F_REACTION in f_replace:
                    rid = f_replace[F_REACTION](rid)
                try:
                    objective_reaction = pamodel.reactions.get_by_id(rid)
                except KeyError:
                    raise CobraSBMLError("Objective reaction '%s' " "not found" % rid)
                try:
                    coefficients[objective_reaction] = number(flux_obj.getCoefficient())
                except ValueError as e:
                    LOGGER.warning(str(e))
    else:
        # some legacy models encode objective coefficients in kinetic laws
        for reaction in model.getListOfReactions():  # type: libsbml.Reaction
            if reaction.isSetKineticLaw():
                klaw = reaction.getKineticLaw()  # type: libsbml.KineticLaw
                p_oc = klaw.getParameter(
                    "OBJECTIVE_COEFFICIENT"
                )  # type: libsbml.LocalParameter
                if p_oc:
                    rid = _check_required(reaction, reaction.getIdAttribute(), "id")
                    if f_replace and F_REACTION in f_replace:
                        rid = f_replace[F_REACTION](rid)
                    try:
                        objective_reaction = pamodel.reactions.get_by_id(rid)
                    except KeyError:
                        raise CobraSBMLError(
                            "Objective reaction '%s' " "not found", rid
                        )
                    try:
                        coefficients[objective_reaction] = number(p_oc.getValue())
                    except ValueError as e:
                        LOGGER.warning(str(e))

                    LOGGER.warning(
                        "Encoding OBJECTIVE_COEFFICIENT in "
                        "KineticLaw is discouraged, "
                        "use fbc:fluxObjective "
                        "instead: %s",
                        reaction,
                    )

    if len(coefficients) == 0:
        LOGGER.error(
            "No objective coefficients in model. Unclear what should " "be optimized"
        )
    set_objective(pamodel, coefficients)
    pamodel.solver.objective.direction = obj_direction

    # parse groups
    model_groups = model.getPlugin("groups")  # type: libsbml.GroupsModelPlugin
    groups = []
    if model_groups:
        # calculate hashmaps to lookup objects in O(1)
        sid_map = {}
        metaid_map = {}
        for obj_list in [
            model.getListOfCompartments(),
            model.getListOfSpecies(),
            model.getListOfReactions(),
            model_groups.getListOfGroups(),
        ]:

            for sbase in obj_list:  # type: libsbml.SBase
                if sbase.isSetId():
                    sid_map[sbase.getIdAttribute()] = sbase
                if sbase.isSetMetaId():
                    metaid_map[sbase.getMetaId()] = sbase

        # create groups
        for group in model_groups.getListOfGroups():  # type: libsbml.Group
            gid = _check_required(group, group.getIdAttribute(), "id")
            if f_replace and F_GROUP in f_replace:
                gid = f_replace[F_GROUP](gid)
            cobra_group = Group(gid)
            cobra_group.name = group.getName()
            if group.isSetKind():
                cobra_group.kind = group.getKindAsString()
            cobra_group.annotation = _parse_annotations(group)
            cobra_group.notes = _parse_notes_dict(group)

            cobra_members = []
            for member in group.getListOfMembers():  # type: libsbml.Member
                if member.isSetIdRef():
                    obj = sid_map[member.getIdRef()]
                elif member.isSetMetaIdRef():
                    obj = metaid_map[member.getMetaIdRef()]

                typecode = obj.getTypeCode()
                obj_id = _check_required(obj, obj.getIdAttribute(), "id")

                # id replacements
                cobra_member = None
                if typecode == libsbml.SBML_SPECIES:
                    if f_replace and F_SPECIE in f_replace:
                        obj_id = f_replace[F_SPECIE](obj_id)
                    try:
                        cobra_member = pamodel.metabolites.get_by_id(obj_id)
                    except KeyError:
                        cobra_member = pamodel.proteins.get_by_id(obj_id)
                elif typecode == libsbml.SBML_REACTION:
                    if f_replace and F_REACTION in f_replace:
                        obj_id = f_replace[F_REACTION](obj_id)
                    cobra_member = pamodel.reactions.get_by_id(obj_id)
                elif typecode == libsbml.SBML_FBC_GENEPRODUCT:
                    if f_replace and F_GENE in f_replace:
                        obj_id = f_replace[F_GENE](obj_id)
                    cobra_member = pamodel.genes.get_by_id(obj_id)
                else:
                    LOGGER.warning(
                        "Member %s could not be added to group %s."
                        "unsupported type code: "
                        "%s" % (member, group, typecode)
                    )

                if cobra_member:
                    cobra_members.append(cobra_member)

            cobra_group.add_members(cobra_members)
            groups.append(cobra_group)
    else:
        # parse deprecated subsystems on reactions
        groups_dict = {}
        for cobra_reaction in pamodel.reactions:
            if "SUBSYSTEM" in cobra_reaction.notes:
                g_name = cobra_reaction.notes["SUBSYSTEM"]
                if g_name in groups_dict:
                    groups_dict[g_name].append(cobra_reaction)
                else:
                    groups_dict[g_name] = [cobra_reaction]

        for gid, cobra_members in groups_dict.items():
            if f_replace and F_GROUP in f_replace:
                gid = f_replace[F_GROUP](gid)
            cobra_group = Group(gid, name=gid, kind="collection")
            cobra_group.add_members(cobra_members)
            groups.append(cobra_group)

    pamodel.add_groups(groups)

    # now add everything under group Proteins to model.proteins if it was not
    # already added based on naming conventions
    if pamodel.groups.query("Protein"):
        g_proteins = pamodel.groups.Protein.members.copy()
        g_proteins = [prot for prot in g_proteins if prot not in pamodel.proteins]
        if g_proteins:
            pamodel.remove_metabolites(g_proteins)
            pamodel.add_enzymes([Enzyme(prot) for prot in g_proteins])

    # general hint for missing flux bounds
    if missing_bounds:
        LOGGER.warning(
            "Missing flux bounds on reactions set to default bounds."
            "As best practise and to avoid confusion flux bounds "
            "should be set explicitly on all reactions."
        )

    return pamodel

def write_sbml_pamodel(
    pa_model: PAModel, filename: str, f_replace=F_REPLACE, units=True
):
    """Write cobra model to filename.

    Enzyme constraint changes: proteins are written as metabolites with
    initialAmount.

    The created model is SBML level 3 version 1 (L1V3) with
    fbc package v2 (fbc-v2).
    If the given filename ends with the suffix ".gz" (for example,
    "myfile.xml.gz"), libSBML assumes the caller wants the file to be
    written compressed in gzip format. Similarly, if the given filename
    ends with ".zip" or ".bz2", libSBML assumes the caller wants the
    file to be compressed in zip or bzip2 format (respectively). Files
    whose names lack these suffixes will be written uncompressed. Special
    considerations for the zip format: If the given filename ends with
    ".zip", the file placed in the zip archive will have the suffix
    ".xml" or ".sbml".  For example, the file in the zip archive will
    be named "test.xml" if the given filename is "test.xml.zip" or
    "test.zip". Similarly, the filename in the archive will be
    "test.sbml" if the given filename is "test.sbml.zip".

    Parameters
    ----------
    cobra_model : PAModelpy.PAModel
        Model instance which is written to SBML
    filename : string
        path to which the model is written
    f_replace: dict of replacement functions for id replacement
    """
    config = Configuration()

    cobra_model = pa_model
    if f_replace is None:
        f_replace = {}

    sbml_ns = libsbml.SBMLNamespaces(3, 1)  # SBML L3V1
    sbml_ns.addPackageNamespace("fbc", 2)  # fbc-v2

    doc: libsbml.SBMLDocument = libsbml.SBMLDocument(sbml_ns)
    doc.setPackageRequired("fbc", False)
    doc.setSBOTerm(SBO_FBA_FRAMEWORK)

    model: libsbml.Model = doc.createModel()
    model_fbc: libsbml.FbcModelPlugin = model.getPlugin("fbc")
    model_fbc.setStrict(True)

    if cobra_model.id is not None:
        model.setId(cobra_model.id)
        model.setMetaId("meta_" + cobra_model.id)
    else:
        model.setMetaId("meta_model")
    if cobra_model.name is not None:
        model.setName(cobra_model.name)

    # for parsing annotation corresponding to the model
    _sbase_annotations(model, cobra_model.annotation)
    # for parsing notes corresponding to the model
    _sbase_notes_dict(model, cobra_model.notes)

    # Meta information (ModelHistory) related to SBMLDocument
    if hasattr(cobra_model, "_sbml"):
        meta = cobra_model._sbml
        if "annotation" in meta:
            _sbase_annotations(doc, meta["annotation"])
        if "notes" in meta:
            _sbase_notes_dict(doc, meta["notes"])

        history: libsbml.ModelHistory = libsbml.ModelHistory()
        if "created" in meta and meta["created"]:
            history.setCreatedDate(meta["created"])
        else:
            time = datetime.datetime.now()
            timestr = time.strftime("%Y-%m-%dT%H:%M:%S")
            date = libsbml.Date(timestr)
            _check(history.setCreatedDate(date), "set creation date")
            _check(history.setModifiedDate(date), "set modified date")

        if "creators" in meta:
            for cobra_creator in meta["creators"]:  # noqa: E501
                creator: libsbml.ModelCreator = libsbml.ModelCreator()
                if cobra_creator.get("familyName", None):
                    creator.setFamilyName(cobra_creator["familyName"])
                if cobra_creator.get("givenName", None):
                    creator.setGivenName(cobra_creator["givenName"])
                if cobra_creator.get("organisation", None):
                    creator.setOrganisation(cobra_creator["organisation"])
                if cobra_creator.get("email", None):
                    creator.setEmail(cobra_creator["email"])

                _check(history.addCreator(creator), "adding creator to ModelHistory.")

        # TODO: Will be implemented as part of
        #  https://github.com/opencobra/cobrapy/issues/810
        # _check(model.setModelHistory(history), 'set model history')

    # Units
    if units:
        flux_udef = model.createUnitDefinition()  # type:libsbml.UnitDefinition
        flux_udef.setId(UNITS_FLUX[0])
        for u in UNITS_FLUX[1]:
            unit = flux_udef.createUnit()  # type: libsbml.Unit
            unit.setKind(u.kind)
            unit.setExponent(u.exponent)
            unit.setScale(u.scale)
            unit.setMultiplier(u.multiplier)

    # minimum and maximum value from model
    if len(cobra_model.reactions) > 0:
        min_value = min(cobra_model.reactions.list_attr("lower_bound"))
        max_value = max(cobra_model.reactions.list_attr("upper_bound"))
    else:
        min_value = config.lower_bound
        max_value = config.upper_bound

    _create_parameter(
        model, pid=LOWER_BOUND_ID, value=min_value, sbo=SBO_DEFAULT_FLUX_BOUND
    )
    _create_parameter(
        model, pid=UPPER_BOUND_ID, value=max_value, sbo=SBO_DEFAULT_FLUX_BOUND
    )
    _create_parameter(model, pid=ZERO_BOUND_ID, value=0, sbo=SBO_DEFAULT_FLUX_BOUND)
    _create_parameter(
        model, pid=BOUND_MINUS_INF, value=-float("Inf"), sbo=SBO_DEFAULT_FLUX_BOUND
    )
    _create_parameter(
        model, pid=BOUND_PLUS_INF, value=float("Inf"), sbo=SBO_DEFAULT_FLUX_BOUND
    )

    # Compartments
    for cid, name in cobra_model.compartments.items():
        compartment: libsbml.Compartment = model.createCompartment()
        compartment.setId(cid)
        compartment.setName(name)
        compartment.setConstant(True)

    # Species
    for metabolite in cobra_model.metabolites:
        specie: libsbml.Species = model.createSpecies()
        specie.setId(
            f_replace[F_SPECIE_REV](metabolite.id)
            if f_replace and F_SPECIE_REV in f_replace
            else metabolite.id
        )
        specie.setConstant(False)
        specie.setBoundaryCondition(False)
        specie.setHasOnlySubstanceUnits(False)
        specie.setName(metabolite.name)
        specie.setCompartment(metabolite.compartment)
        s_fbc: libsbml.FbcSpeciesPlugin = specie.getPlugin("fbc")
        if metabolite.charge is not None:
            s_fbc.setCharge(int(metabolite.charge))
        if metabolite.formula is not None:
            s_fbc.setChemicalFormula(metabolite.formula)

        _sbase_annotations(specie, metabolite.annotation)
        _sbase_notes_dict(specie, metabolite.notes)

    #enzyme
    tot_prot_constraints = {}
    for enzyme in pa_model.enzymes:
        specie: libsbml.Species = model.createSpecies()
        sid = enzyme.id
        if f_replace and F_SPECIE_REV in f_replace:
            sid = f_replace[F_SPECIE_REV](sid)
        specie.setId(sid)
        specie.setConstant(False)
        specie.setBoundaryCondition(False)
        specie.setHasOnlySubstanceUnits(False)
        specie.setName('EC_'+enzyme.id)
        # if isinstance(enzyme.concentration, numbers.Number) and not isnan(
        #     enzyme.concentration
        # ):
        #     specie.setInitialAmount(enzyme.concentration)

        _sbase_annotations(specie, enzyme.annotation)
        tot_prot_constraints[specie.getId()] = -enzyme.molmass * 1e-6

    # Genes
    for cobra_gene in cobra_model.genes:
        gp: libsbml.GeneProduct = model_fbc.createGeneProduct()
        gid = cobra_gene.id
        if f_replace and F_GENE_REV in f_replace:
            gid = f_replace[F_GENE_REV](gid)
        gp.setId(gid)
        gname = cobra_gene.name
        if gname is None or len(gname) == 0:
            gname = gid
        gp.setName(gname)
        gp.setLabel(gid)

        _sbase_annotations(gp, cobra_gene.annotation)
        _sbase_notes_dict(gp, cobra_gene.notes)

    # Objective
    objective: libsbml.Objective = model_fbc.createObjective()
    objective.setId("obj")
    objective.setType(SHORT_LONG_DIRECTION[cobra_model.objective.direction])
    model_fbc.setActiveObjectiveId("obj")

    # Reactions
    reaction_coefficients = linear_reaction_coefficients(cobra_model)
    for cobra_reaction in cobra_model.reactions:
        rid = cobra_reaction.id
        if f_replace and F_REACTION_REV in f_replace:
            rid = f_replace[F_REACTION_REV](rid)
        reaction: libsbml.Reaction = model.createReaction()
        reaction.setId(rid)
        reaction.setName(cobra_reaction.name)
        reaction.setFast(False)
        reaction.setReversible((cobra_reaction.lower_bound < 0))
        _sbase_annotations(reaction, cobra_reaction.annotation)
        _sbase_notes_dict(reaction, cobra_reaction.notes)

        # stoichiometry
        for metabolite, stoichiometry in cobra_reaction._metabolites.items():
            sid = metabolite.id
            if f_replace and F_SPECIE_REV in f_replace:
                sid = f_replace[F_SPECIE_REV](sid)
            if stoichiometry < 0:
                sref = (
                    reaction.createReactant()
                )  # noqa: E501 type: libsbml.SpeciesReference
                sref.setSpecies(sid)
                sref.setStoichiometry(-stoichiometry)
                sref.setConstant(True)
            else:
                sref = (
                    reaction.createProduct()
                )  # noqa: E501 type: libsbml.SpeciesReference
                sref.setSpecies(sid)
                sref.setStoichiometry(stoichiometry)
                sref.setConstant(True)

        # bounds
        r_fbc: libsbml.FbcReactionPlugin = reaction.getPlugin("fbc")
        r_fbc.setLowerFluxBound(
            _create_bound(
                model,
                cobra_reaction,
                "lower_bound",
                f_replace=f_replace,
                units=units,
                flux_udef=flux_udef,
            )
        )
        r_fbc.setUpperFluxBound(
            _create_bound(
                model,
                cobra_reaction,
                "upper_bound",
                f_replace=f_replace,
                units=units,
                flux_udef=flux_udef,
            )
        )

        # GPR
        gpr = cobra_reaction.gene_reaction_rule
        if gpr is not None and len(gpr) > 0:

            # replace ids in string
            if f_replace and F_GENE_REV in f_replace:
                gpr = gpr.replace("(", "( ")
                gpr = gpr.replace(")", " )")
                tokens = gpr.split()

                for k in range(len(tokens)):
                    if tokens[k] not in ["and", "or", "(", ")"]:
                        tokens[k] = f_replace[F_GENE_REV](tokens[k])
                gpr_new = " ".join(tokens)
            else:
                gpr_new = gpr

            gpa: libsbml.GeneProductAssociation = (
                r_fbc.createGeneProductAssociation()
            )  # noqa: E501
            # uses ids to identify GeneProducts (True),
            # does not create GeneProducts (False)
            _check(gpa.setAssociation(gpr_new, True, False), "set gpr: " + gpr_new)

        # objective coefficients
        if reaction_coefficients.get(cobra_reaction, 0) != 0:
            flux_obj: libsbml.FluxObjective = (
                objective.createFluxObjective()
            )  # noqa: E501
            flux_obj.setReaction(rid)
            flux_obj.setCoefficient(cobra_reaction.objective_coefficient)

    #CatalyticEvents
    for catalytic_event in cobra_model.catalytic_events:
        rid = catalytic_event.id
        if f_replace and F_REACTION_REV in f_replace:
            rid = f_replace[F_REACTION_REV](rid)
        ce_reaction: libsbml.Reaction = model.createReaction()
        ce_reaction.setId(rid)
        ce_reaction.setName(catalytic_event.name)
        ce_reaction.setFast(False)
        ce_reaction.setReversible((catalytic_event.lower_bound < 0))
        _sbase_annotations(ce_reaction, catalytic_event.annotation)
        _sbase_notes_dict(ce_reaction, catalytic_event.notes)

        # stoichiometry
        for enzyme in catalytic_event.enzymes:
            for constraint in enzyme._constraints:
                sid = constraint.id
                if constraint.id[-1] in catalytic_event.kcats[enzyme].keys():
                    stoichiometry = catalytic_event.kcats[enzyme][constraint.id[-1]] * 3600 * 1e-6
                else:
                    continue
                if f_replace and F_SPECIE_REV in f_replace:
                    sid = f_replace[F_SPECIE_REV](sid)
                if stoichiometry < 0:
                    sref = (
                        ce_reaction.createReactant()
                    )  # noqa: E501 type: libsbml.SpeciesReference
                    sref.setSpecies(sid)
                    sref.setStoichiometry(-stoichiometry)
                    sref.setConstant(True)
                else:
                    sref = (
                        ce_reaction.createProduct()
                    )  # noqa: E501 type: libsbml.SpeciesReference
                    sref.setSpecies(sid)
                    sref.setStoichiometry(stoichiometry)
                    sref.setConstant(True)

        # bounds
        r_fbc: libsbml.FbcReactionPlugin = ce_reaction.getPlugin("fbc")
        r_fbc.setLowerFluxBound(
            _create_bound(
                model,
                catalytic_event,
                "lower_bound",
                f_replace=f_replace,
                units=units,
                flux_udef=flux_udef,
            )
        )
        r_fbc.setUpperFluxBound(
            _create_bound(
                model,
                catalytic_event,
                "upper_bound",
                f_replace=f_replace,
                units=units,
                flux_udef=flux_udef,
            )
        )

    #sectors
    for sector in cobra_model.sectors:
        if not isinstance(sector, ActiveEnzymeSector):
            for var in sector.variables:
                variable = var
                rid = var.name
                if f_replace and F_REACTION_REV in f_replace:
                    rid = f_replace[F_REACTION_REV](rid)
                var: libsbml.Reaction = model.createReaction()
                var.setId(rid)
                var.setName(rid)
                var.setFast(False)
                var.setReversible((False))
                _sbase_annotations(var, {'type':'Variable'})

                # stoichiometry
                for constraint in sector.constraints:
                    #firs add constraint as a species
                    specie: libsbml.Species = model.createSpecies()
                    specie.setId(
                        f_replace[F_SPECIE_REV](constraint.name)
                        if f_replace and F_SPECIE_REV in f_replace
                        else constraint.id
                    )
                    specie.setConstant(False)
                    specie.setBoundaryCondition(False)
                    specie.setHasOnlySubstanceUnits(False)
                    specie.setName(constraint.name)

                    tot_prot_constraints[specie.getId()] = -sector.mol_mass[0] * 1e-6

                    #add constraint to variable
                    sid = constraint.name
                    if isinstance(variable, Constant):
                        variable = cobra_model.variables[variable.id]
                    lin_coef = constraint.get_linear_coefficients([variable])
                    stoichiometry = lin_coef[variable]
                    if f_replace and F_SPECIE_REV in f_replace:
                        sid = f_replace[F_SPECIE_REV](sid)
                    if stoichiometry < 0:
                        sref = (
                            var.createReactant()
                        )  # noqa: E501 type: libsbml.SpeciesReference
                        sref.setSpecies(sid)
                        sref.setStoichiometry(-stoichiometry)
                        sref.setConstant(True)
                    else:
                        sref = (
                            var.createProduct()
                        )  # noqa: E501 type: libsbml.SpeciesReference
                        sref.setSpecies(sid)
                        sref.setStoichiometry(stoichiometry)
                        sref.setConstant(True)

                # bounds
                r_fbc: libsbml.FbcReactionPlugin = var.getPlugin("fbc")
                r_fbc.setLowerFluxBound(
                    _create_bound_var(
                        model,
                        variable,
                        "lb",
                        f_replace=f_replace,
                        units=units,
                        flux_udef=flux_udef,
                    )
                )
                r_fbc.setUpperFluxBound(
                    _create_bound_var(
                        model,
                        variable,
                        "ub",
                        f_replace=f_replace,
                        units=units,
                        flux_udef=flux_udef,
                    )
                )

    # Total Protein Constraint
    tpc = cobra_model.constraints[cobra_model.TOTAL_PROTEIN_CONSTRAINT_ID]
    specie: libsbml.Species = model.createSpecies()
    specie.setId(
        f_replace[F_SPECIE_REV](tpc.name)
        if f_replace and F_SPECIE_REV in f_replace
        else tpc.id
    )
    specie.setConstant(False)
    specie.setBoundaryCondition(False)
    specie.setHasOnlySubstanceUnits(False)
    specie.setName(tpc.name)

    tot_prot_constraints[tpc.name] = 1.0

    tpc_var = cobra_model.variables['R_' + cobra_model.TOTAL_PROTEIN_CONSTRAINT_ID]
    rid = tpc_var.name
    if f_replace and F_REACTION_REV in f_replace:
        rid = f_replace[F_REACTION_REV](rid)
    var: libsbml.Reaction = model.createReaction()
    var.setId(rid)
    var.setName(rid)
    var.setFast(False)
    var.setReversible((False))

    for sid, stoichiometry in tot_prot_constraints.items():
        if stoichiometry < 0:
            sref = (
                var.createReactant()
            )  # noqa: E501 type: libsbml.SpeciesReference
            sref.setSpecies(sid)
            sref.setStoichiometry(-stoichiometry)
            sref.setConstant(True)
        else:
            sref = (
                var.createProduct()
            )  # noqa: E501 type: libsbml.SpeciesReference
            sref.setSpecies(sid)
            sref.setStoichiometry(stoichiometry)
            sref.setConstant(True)

        # bounds
    r_fbc: libsbml.FbcReactionPlugin = var.getPlugin("fbc")
    r_fbc.setLowerFluxBound(
        _create_bound_var(
            model,
            tpc_var,
            "lb",
            f_replace=f_replace,
            units=units,
            flux_udef=flux_udef,
        )
    )
    r_fbc.setUpperFluxBound(
        _create_bound_var(
            model,
            tpc_var,
            "ub",
            f_replace=f_replace,
            units=units,
            flux_udef=flux_udef,
        )
    )

    # write groups
    if len(cobra_model.groups) > 0:
        doc.enablePackage(
            "http://www.sbml.org/sbml/level3/version1/groups/version1", "groups", True
        )
        doc.setPackageRequired("groups", False)
        model_group: libsbml.GroupsModelPlugin = model.getPlugin("groups")  # noqa: E501
        for cobra_group in cobra_model.groups:
            group: libsbml.Group = model_group.createGroup()
            if f_replace and F_GROUP_REV in f_replace:
                gid = f_replace[F_GROUP_REV](cobra_group.id)
            else:
                gid = cobra_group.id
            group.setId(gid)
            group.setName(cobra_group.name)
            group.setKind(cobra_group.kind)

            _sbase_notes_dict(group, cobra_group.notes)
            _sbase_annotations(group, cobra_group.annotation)

            for cobra_member in cobra_group.members:
                member: libsbml.Member = group.createMember()
                mid = cobra_member.id
                m_type = str(type(cobra_member))

                # id replacements
                if "Reaction" in m_type:
                    if f_replace and F_REACTION_REV in f_replace:
                        mid = f_replace[F_REACTION_REV](mid)
                if "Metabolite" in m_type or "Protein" in m_type:
                    if f_replace and F_SPECIE_REV in f_replace:
                        mid = f_replace[F_SPECIE_REV](mid)
                if "Gene" in m_type:
                    if f_replace and F_GENE_REV in f_replace:
                        mid = f_replace[F_GENE_REV](mid)

                member.setIdRef(mid)
                if cobra_member.name and len(cobra_member.name) > 0:
                    member.setName(cobra_member.name)

    if isinstance(filename, str):
        # write to path
        libsbml.writeSBMLToFile(doc, filename)

    elif hasattr(filename, "write"):
        # write to file handle
        sbml_str = libsbml.writeSBMLToString(doc)
        filename.write(sbml_str)

def _create_bound_var(
    model: libsbml.Model,
    variable,
    bound_type: str,
    f_replace: dict,
    units: Optional[bool] = None,
    flux_udef: Optional[libsbml.UnitDefinition] = None,
) -> str:
    """Create bound in model for given variable.

    Adds the parameters for the bounds to the SBML model.

    Parameters
    ----------
    model : libsbml.Model
        SBML model instance
    reaction : optlang.Variable
        optlang Variable instance from which the bounds are read.
    bound_type : {LOWER_BOUND, UPPER_BOUND}
        Type of bound
    f_replace : dict
        of id replacement functions
    units : bool, optional, defualt None
        Whether or not to use flux units in the SBML document.
    flux_udef: libsbml.UnitDefinition, optional
        Unit definition if units are used.

    Returns
    -------
    pid: str
        Id of bound parameter.
    """
    value = getattr(variable, bound_type)
    if value == config.lower_bound:
        return LOWER_BOUND_ID
    elif value == 0:
        return ZERO_BOUND_ID
    elif value == config.upper_bound:
        return UPPER_BOUND_ID
    elif value == -float("Inf"):
        return BOUND_MINUS_INF
    elif value == float("Inf"):
        return BOUND_PLUS_INF
    else:
        if value is None:
            if bound_type == 'lb':
                value = 0
            if bound_type == 'ub':
                value = 1000
        # new parameter
        vid = variable.name
        if f_replace and F_REACTION_REV in f_replace:
            vid = f_replace[F_REACTION_REV](vid)
        pid = vid + "_" + bound_type
        _create_parameter(
            model,
            pid=pid,
            value=value,
            sbo=SBO_FLUX_BOUND,
            units=units,
            flux_udef=flux_udef,
        )
        return pid