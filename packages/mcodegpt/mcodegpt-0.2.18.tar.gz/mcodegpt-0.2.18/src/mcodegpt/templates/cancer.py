"""Core template."""
from __future__ import annotations

from typing import Any, List, Optional


from pydantic.v1 import BaseModel as BaseModel
from pydantic.v1 import Field

metamodel_version = "None"
version = "None"


class WeakRefShimBaseModel(BaseModel):
    __slots__ = "__weakref__"


class ConfiguredBaseModel(
    WeakRefShimBaseModel,
    validate_assignment=True,
    validate_all=True,
    underscore_attrs_are_private=True,
    extra="forbid",
    arbitrary_types_allowed=True,
):
    pass


class ExtractionResult(ConfiguredBaseModel):
    """A result of extracting knowledge on text."""

    input_id: Optional[str] = Field(None)
    input_title: Optional[str] = Field(None)
    input_text: Optional[str] = Field(None)
    raw_completion_output: Optional[str] = Field(None)
    prompt: Optional[str] = Field(None)
    extracted_object: Optional[Any] = Field(
        None, description="""The complex objects extracted from the text"""
    )
    named_entities: Optional[List[Any]] = Field(
        default_factory=list, description="""Named entities extracted from the text"""
    )

class CancerAnnotations(ConfiguredBaseModel):
    people: Optional[List[str]] = Field(
        default_factory= list, description="""the name of a person"""
    )


    human_specimen_identifier: Optional[List[str]] = Field(
        default_factory= list, description="""What is the identifier for the human specimen?"""
    )
    

    human_specimen_collection_site: Optional[List[str]] = Field(
        default_factory= list, description="""Where was the human specimen collected from?"""
    )
    

    human_specimen_specimen_type: Optional[List[str]] = Field(
        default_factory= list, description="""What type of specimen is the human specimen?"""
    )
    

    name: Optional[List[str]] = Field(
        default_factory= list, description="""What is the name of the patient?"""
    )
    

    contact_info: Optional[List[str]] = Field(
        default_factory= list, description="""What is the patient's contact information?"""
    )
    

    birth_date: Optional[List[str]] = Field(
        default_factory= list, description="""What is the patient's birth date?"""
    )
    

    gender: Optional[List[str]] = Field(
        default_factory= list, description="""What is the patient's gender?"""
    )
    

    zip_code: Optional[List[str]] = Field(
        default_factory= list, description="""What is the patient's zip code?"""
    )
    

    us_core_race: Optional[List[str]] = Field(
        default_factory= list, description="""What is the patient's recorded race (US Core standard)?"""
    )
    

    us_core_birth_sex: Optional[List[str]] = Field(
        default_factory= list, description="""What is the patient's birth sex (US Core standard)?"""
    )
    

    us_core_ethnicity: Optional[List[str]] = Field(
        default_factory= list, description="""What is the patient's ethnicity (US Core standard)?"""
    )
    

    death_date: Optional[List[str]] = Field(
        default_factory= list, description="""What is the patient's date of death?"""
    )
    

    disease_status_evidence_type: Optional[List[str]] = Field(
        default_factory= list, description="""What type of evidence indicates the disease status?"""
    )
    

    tumor_identifier: Optional[List[str]] = Field(
        default_factory= list, description="""What is the identifier for the tumor?"""
    )
    

    tumor_body_location: Optional[List[str]] = Field(
        default_factory= list, description="""Where is the tumor located in the body?"""
    )
    

    tumor_size_longest_dimension: Optional[List[str]] = Field(
        default_factory= list, description="""What is the tumor's longest dimension?"""
    )
    

    cancer_stage_stage_type: Optional[List[str]] = Field(
        default_factory= list, description="""What type of cancer stage is identified?"""
    )
    

    cancer_asserted_date: Optional[List[str]] = Field(
        default_factory= list, description="""What date was the cancer asserted?"""
    )
    

    cancer_body_site: Optional[List[str]] = Field(
        default_factory= list, description="""What body site is affected by the cancer?"""
    )
    

    tumor_marker_test_result_value: Optional[List[str]] = Field(
        default_factory= list, description="""What is the result value of the tumor marker test?"""
    )
    

    people_human_specimen_identifier_interaction: Optional[List[People_Human_Specimen_Identifier_Interaction]] = Field(
        default_factory=list, description="""list of what people has Human Specimen Identifier, separated by semi-colons"""
    )
    

    people_human_specimen_collection_site_interaction: Optional[List[People_Human_Specimen_Collection_Site_Interaction]] = Field(
        default_factory=list, description="""list of what people has Human Specimen Collection Site, separated by semi-colons"""
    )
    

    people_human_specimen_specimen_type_interaction: Optional[List[People_Human_Specimen_Specimen_Type_Interaction]] = Field(
        default_factory=list, description="""list of what people has Human Specimen Specimen Type, separated by semi-colons"""
    )
    

    people_name_interaction: Optional[List[People_Name_Interaction]] = Field(
        default_factory=list, description="""list of what people has Name, separated by semi-colons"""
    )
    

    people_contact_info_interaction: Optional[List[People_Contact_Info_Interaction]] = Field(
        default_factory=list, description="""list of what people has Contact Info, separated by semi-colons"""
    )
    

    people_birth_date_interaction: Optional[List[People_Birth_Date_Interaction]] = Field(
        default_factory=list, description="""list of what people has Birth Date, separated by semi-colons"""
    )
    

    people_gender_interaction: Optional[List[People_Gender_Interaction]] = Field(
        default_factory=list, description="""list of what people has Gender, separated by semi-colons"""
    )
    

    people_zip_code_interaction: Optional[List[People_Zip_Code_Interaction]] = Field(
        default_factory=list, description="""list of what people has Zip Code, separated by semi-colons"""
    )
    

    people_us_core_race_interaction: Optional[List[People_Us_Core_Race_Interaction]] = Field(
        default_factory=list, description="""list of what people has US Core Race, separated by semi-colons"""
    )
    

    people_us_core_birth_sex_interaction: Optional[List[People_Us_Core_Birth_Sex_Interaction]] = Field(
        default_factory=list, description="""list of what people has US Core Birth Sex, separated by semi-colons"""
    )
    

    people_us_core_ethnicity_interaction: Optional[List[People_Us_Core_Ethnicity_Interaction]] = Field(
        default_factory=list, description="""list of what people has US Core Ethnicity, separated by semi-colons"""
    )
    

    people_death_date_interaction: Optional[List[People_Death_Date_Interaction]] = Field(
        default_factory=list, description="""list of what people has Death Date, separated by semi-colons"""
    )
    

    people_disease_status_evidence_type_interaction: Optional[List[People_Disease_Status_Evidence_Type_Interaction]] = Field(
        default_factory=list, description="""list of what people has Disease Status Evidence Type, separated by semi-colons"""
    )
    

    people_tumor_identifier_interaction: Optional[List[People_Tumor_Identifier_Interaction]] = Field(
        default_factory=list, description="""list of what people has Tumor Identifier, separated by semi-colons"""
    )
    

    people_tumor_body_location_interaction: Optional[List[People_Tumor_Body_Location_Interaction]] = Field(
        default_factory=list, description="""list of what people has Tumor Body Location, separated by semi-colons"""
    )
    

    people_tumor_size_longest_dimension_interaction: Optional[List[People_Tumor_Size_Longest_Dimension_Interaction]] = Field(
        default_factory=list, description="""list of what people has Tumor Size Longest Dimension, separated by semi-colons"""
    )
    

    people_cancer_stage_stage_type_interaction: Optional[List[People_Cancer_Stage_Stage_Type_Interaction]] = Field(
        default_factory=list, description="""list of what people has Cancer Stage Stage Type, separated by semi-colons"""
    )
    

    people_cancer_asserted_date_interaction: Optional[List[People_Cancer_Asserted_Date_Interaction]] = Field(
        default_factory=list, description="""list of what people has Cancer Asserted Date, separated by semi-colons"""
    )
    

    people_cancer_body_site_interaction: Optional[List[People_Cancer_Body_Site_Interaction]] = Field(
        default_factory=list, description="""list of what people has Cancer Body Site, separated by semi-colons"""
    )
    

    people_tumor_marker_test_result_value_interaction: Optional[List[People_Tumor_Marker_Test_Result_Value_Interaction]] = Field(
        default_factory=list, description="""list of what people has Tumor Marker Test Result Value, separated by semi-colons"""
    )


class NamedEntity(ConfiguredBaseModel):
    id: Optional[str] = Field(None, description="""A unique identifier for the named entity""")
    label: Optional[str] = Field(None, description="""The label (name) of the named thing""")

# +
class Human_Specimen_Identifier(NamedEntity):
    id: Optional[str] = Field(None, description="""A unique identifier for the named entity""")
    label: Optional[str] = Field(None, description="""What is the identifier for the human specimen?""")
    

class Human_Specimen_Collection_Site(NamedEntity):
    id: Optional[str] = Field(None, description="""A unique identifier for the named entity""")
    label: Optional[str] = Field(None, description="""Where was the human specimen collected from?""")
    

class Human_Specimen_Specimen_Type(NamedEntity):
    id: Optional[str] = Field(None, description="""A unique identifier for the named entity""")
    label: Optional[str] = Field(None, description="""What type of specimen is the human specimen?""")
    

class Name(NamedEntity):
    id: Optional[str] = Field(None, description="""A unique identifier for the named entity""")
    label: Optional[str] = Field(None, description="""What is the name of the patient?""")
    

class Contact_Info(NamedEntity):
    id: Optional[str] = Field(None, description="""A unique identifier for the named entity""")
    label: Optional[str] = Field(None, description="""What is the patient's contact information?""")
    

class Birth_Date(NamedEntity):
    id: Optional[str] = Field(None, description="""A unique identifier for the named entity""")
    label: Optional[str] = Field(None, description="""What is the patient's birth date?""")
    

class Gender(NamedEntity):
    id: Optional[str] = Field(None, description="""A unique identifier for the named entity""")
    label: Optional[str] = Field(None, description="""What is the patient's gender?""")
    

class Zip_Code(NamedEntity):
    id: Optional[str] = Field(None, description="""A unique identifier for the named entity""")
    label: Optional[str] = Field(None, description="""What is the patient's zip code?""")
    

class Us_Core_Race(NamedEntity):
    id: Optional[str] = Field(None, description="""A unique identifier for the named entity""")
    label: Optional[str] = Field(None, description="""What is the patient's recorded race (US Core standard)?""")
    

class Us_Core_Birth_Sex(NamedEntity):
    id: Optional[str] = Field(None, description="""A unique identifier for the named entity""")
    label: Optional[str] = Field(None, description="""What is the patient's birth sex (US Core standard)?""")
    

class Us_Core_Ethnicity(NamedEntity):
    id: Optional[str] = Field(None, description="""A unique identifier for the named entity""")
    label: Optional[str] = Field(None, description="""What is the patient's ethnicity (US Core standard)?""")
    

class Death_Date(NamedEntity):
    id: Optional[str] = Field(None, description="""A unique identifier for the named entity""")
    label: Optional[str] = Field(None, description="""What is the patient's date of death?""")
    

class Disease_Status_Evidence_Type(NamedEntity):
    id: Optional[str] = Field(None, description="""A unique identifier for the named entity""")
    label: Optional[str] = Field(None, description="""What type of evidence indicates the disease status?""")
    

class Tumor_Identifier(NamedEntity):
    id: Optional[str] = Field(None, description="""A unique identifier for the named entity""")
    label: Optional[str] = Field(None, description="""What is the identifier for the tumor?""")
    

class Tumor_Body_Location(NamedEntity):
    id: Optional[str] = Field(None, description="""A unique identifier for the named entity""")
    label: Optional[str] = Field(None, description="""Where is the tumor located in the body?""")
    

class Tumor_Size_Longest_Dimension(NamedEntity):
    id: Optional[str] = Field(None, description="""A unique identifier for the named entity""")
    label: Optional[str] = Field(None, description="""What is the tumor's longest dimension?""")
    

class Cancer_Stage_Stage_Type(NamedEntity):
    id: Optional[str] = Field(None, description="""A unique identifier for the named entity""")
    label: Optional[str] = Field(None, description="""What type of cancer stage is identified?""")
    

class Cancer_Asserted_Date(NamedEntity):
    id: Optional[str] = Field(None, description="""A unique identifier for the named entity""")
    label: Optional[str] = Field(None, description="""What date was the cancer asserted?""")
    

class Cancer_Body_Site(NamedEntity):
    id: Optional[str] = Field(None, description="""A unique identifier for the named entity""")
    label: Optional[str] = Field(None, description="""What body site is affected by the cancer?""")
    

class Tumor_Marker_Test_Result_Value(NamedEntity):
    id: Optional[str] = Field(None, description="""A unique identifier for the named entity""")
    label: Optional[str] = Field(None, description="""What is the result value of the tumor marker test?""")


# -

class CompoundExpression(ConfiguredBaseModel):
    pass

# +
class People_Human_Specimen_Identifier_Interaction(CompoundExpression):
    people: Optional[str] = Field(None)
    human_specimen_identifier: Optional[str] = Field(None)
    

class People_Human_Specimen_Collection_Site_Interaction(CompoundExpression):
    people: Optional[str] = Field(None)
    human_specimen_collection_site: Optional[str] = Field(None)
    

class People_Human_Specimen_Specimen_Type_Interaction(CompoundExpression):
    people: Optional[str] = Field(None)
    human_specimen_specimen_type: Optional[str] = Field(None)
    

class People_Name_Interaction(CompoundExpression):
    people: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    

class People_Contact_Info_Interaction(CompoundExpression):
    people: Optional[str] = Field(None)
    contact_info: Optional[str] = Field(None)
    

class People_Birth_Date_Interaction(CompoundExpression):
    people: Optional[str] = Field(None)
    birth_date: Optional[str] = Field(None)
    

class People_Gender_Interaction(CompoundExpression):
    people: Optional[str] = Field(None)
    gender: Optional[str] = Field(None)
    

class People_Zip_Code_Interaction(CompoundExpression):
    people: Optional[str] = Field(None)
    zip_code: Optional[str] = Field(None)
    

class People_Us_Core_Race_Interaction(CompoundExpression):
    people: Optional[str] = Field(None)
    us_core_race: Optional[str] = Field(None)
    

class People_Us_Core_Birth_Sex_Interaction(CompoundExpression):
    people: Optional[str] = Field(None)
    us_core_birth_sex: Optional[str] = Field(None)
    

class People_Us_Core_Ethnicity_Interaction(CompoundExpression):
    people: Optional[str] = Field(None)
    us_core_ethnicity: Optional[str] = Field(None)
    

class People_Death_Date_Interaction(CompoundExpression):
    people: Optional[str] = Field(None)
    death_date: Optional[str] = Field(None)
    

class People_Disease_Status_Evidence_Type_Interaction(CompoundExpression):
    people: Optional[str] = Field(None)
    disease_status_evidence_type: Optional[str] = Field(None)
    

class People_Tumor_Identifier_Interaction(CompoundExpression):
    people: Optional[str] = Field(None)
    tumor_identifier: Optional[str] = Field(None)
    

class People_Tumor_Body_Location_Interaction(CompoundExpression):
    people: Optional[str] = Field(None)
    tumor_body_location: Optional[str] = Field(None)
    

class People_Tumor_Size_Longest_Dimension_Interaction(CompoundExpression):
    people: Optional[str] = Field(None)
    tumor_size_longest_dimension: Optional[str] = Field(None)
    

class People_Cancer_Stage_Stage_Type_Interaction(CompoundExpression):
    people: Optional[str] = Field(None)
    cancer_stage_stage_type: Optional[str] = Field(None)
    

class People_Cancer_Asserted_Date_Interaction(CompoundExpression):
    people: Optional[str] = Field(None)
    cancer_asserted_date: Optional[str] = Field(None)
    

class People_Cancer_Body_Site_Interaction(CompoundExpression):
    people: Optional[str] = Field(None)
    cancer_body_site: Optional[str] = Field(None)
    

class People_Tumor_Marker_Test_Result_Value_Interaction(CompoundExpression):
    people: Optional[str] = Field(None)
    tumor_marker_test_result_value: Optional[str] = Field(None)
    


# -

class Triple(CompoundExpression):
    """Abstract parent for Relation Extraction tasks."""

    subject: Optional[str] = Field(None)
    predicate: Optional[str] = Field(None)
    object: Optional[str] = Field(None)
    qualifier: Optional[str] = Field(
        None, description="""A qualifier for the statements, e.g. \"NOT\" for negation"""
    )
    subject_qualifier: Optional[str] = Field(
        None,
        description="""An optional qualifier or modifier for the subject of the\
            statement, e.g. \"high dose\" or \"intravenously administered\"""",
    )
    object_qualifier: Optional[str] = Field(
        None,
        description="""An optional qualifier or modifier for the object of\
            the statement, e.g. \"severe\" or \"with additional complications\"""",
    )


class TextWithTriples(ConfiguredBaseModel):
    publication: Optional[Publication] = Field(None)
    triples: Optional[List[Triple]] = Field(default_factory=list)


class RelationshipType(NamedEntity):
    id: Optional[str] = Field(None, description="""A unique identifier for the named entity""")
    label: Optional[str] = Field(None, description="""The label (name) of the named thing""")


class Publication(ConfiguredBaseModel):
    id: Optional[str] = Field(None, description="""The publication identifier""")
    title: Optional[str] = Field(None, description="""The title of the publication""")
    abstract: Optional[str] = Field(None, description="""The abstract of the publication""")
    combined_text: Optional[str] = Field(None)
    full_text: Optional[str] = Field(None, description="""The full text of the publication""")


class AnnotatorResult(ConfiguredBaseModel):
    subject_text: Optional[str] = Field(None)
    object_id: Optional[str] = Field(None)
    object_text: Optional[str] = Field(None)


# +
# Update forward refs
# see https://pydantic-docs.helpmanual.io/usage/postponed_annotations/
# CancerAnnotations.update_forward_refs()
ExtractionResult.update_forward_refs()
NamedEntity.update_forward_refs()
# People.update_forward_refs()
# Cancer.update_forward_refs()
CompoundExpression.update_forward_refs()
# PeopleCancerRelationship.update_forward_refs()
Triple.update_forward_refs()
TextWithTriples.update_forward_refs()
RelationshipType.update_forward_refs()
Publication.update_forward_refs()
AnnotatorResult.update_forward_refs()

CancerAnnotations.update_forward_refs()

Human_Specimen_Identifier.update_forward_refs()
    

Human_Specimen_Collection_Site.update_forward_refs()
    

Human_Specimen_Specimen_Type.update_forward_refs()
    

Name.update_forward_refs()
    

Contact_Info.update_forward_refs()
    

Birth_Date.update_forward_refs()
    

Gender.update_forward_refs()
    

Zip_Code.update_forward_refs()
    

Us_Core_Race.update_forward_refs()
    

Us_Core_Birth_Sex.update_forward_refs()
    

Us_Core_Ethnicity.update_forward_refs()
    

Death_Date.update_forward_refs()
    

Disease_Status_Evidence_Type.update_forward_refs()
    

Tumor_Identifier.update_forward_refs()
    

Tumor_Body_Location.update_forward_refs()
    

Tumor_Size_Longest_Dimension.update_forward_refs()
    

Cancer_Stage_Stage_Type.update_forward_refs()
    

Cancer_Asserted_Date.update_forward_refs()
    

Cancer_Body_Site.update_forward_refs()
    

Tumor_Marker_Test_Result_Value.update_forward_refs()
    

People_Human_Specimen_Identifier_Interaction.update_forward_refs()
    

People_Human_Specimen_Collection_Site_Interaction.update_forward_refs()
    

People_Human_Specimen_Specimen_Type_Interaction.update_forward_refs()
    

People_Name_Interaction.update_forward_refs()
    

People_Contact_Info_Interaction.update_forward_refs()
    

People_Birth_Date_Interaction.update_forward_refs()
    

People_Gender_Interaction.update_forward_refs()
    

People_Zip_Code_Interaction.update_forward_refs()
    

People_Us_Core_Race_Interaction.update_forward_refs()
    

People_Us_Core_Birth_Sex_Interaction.update_forward_refs()
    

People_Us_Core_Ethnicity_Interaction.update_forward_refs()
    

People_Death_Date_Interaction.update_forward_refs()
    

People_Disease_Status_Evidence_Type_Interaction.update_forward_refs()
    

People_Tumor_Identifier_Interaction.update_forward_refs()
    

People_Tumor_Body_Location_Interaction.update_forward_refs()
    

People_Tumor_Size_Longest_Dimension_Interaction.update_forward_refs()
    

People_Cancer_Stage_Stage_Type_Interaction.update_forward_refs()
    

People_Cancer_Asserted_Date_Interaction.update_forward_refs()
    

People_Cancer_Body_Site_Interaction.update_forward_refs()
    

People_Tumor_Marker_Test_Result_Value_Interaction.update_forward_refs()
    
    
