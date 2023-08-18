from pydantic import BaseModel, validator
from typing import List, Optional
from datetime import date
import numpy as np
from scipy.spatial.distance import euclidean,cosine
from strsimpy.normalized_levenshtein import NormalizedLevenshtein
from tagline_embedding import *

DOT_PRODUCT='dot_product'
EUCLIDEAN='euclidean'
COSINE='cosine'

DEFAULT_DISTANCE_METRIC=COSINE
DEFAULT_DISTANCE_THRESHOLD=0.1 #if distance metric>= DISTANCE_THRESHOLD then two Descriptions are considered semantically different

normalized_levenshtein = NormalizedLevenshtein() #difference metric between strings used to see if two names are the same
NORMALIZED_LEVENSHTEIN_THRESHOLD=0.1

def same_string(str_0: str, str_1:str) -> bool:
    '''The function checks if two strings are the same by comparing their normalized Levenshtein distance
    and checking if one string is a substring of the other.
    
    Parameters
    ----------
    str_0 : str
    str_1 : str
    
    Returns
    -------
        a boolean value. If the two input strings are the same or similar enough based on the normalized
    Levenshtein distance, it returns True. Otherwise, it returns False.
    
    '''
    if str_0.find(str_1)!=-1 or str_1.find(str_0)!=-1:
        return True
    if normalized_levenshtein.distance(str_0, str_1) >= NORMALIZED_LEVENSHTEIN_THRESHOLD:
        return False
    return True

class DescriptionModel(BaseModel): #text description + embedding
    Text: Optional[str]
    Embedding: Optional[List[float]] #if there is a text description, we can compute the vector embedding
    DistanceMetric: str = DEFAULT_DISTANCE_METRIC
    DistanceThreshold: float = DEFAULT_DISTANCE_THRESHOLD

    @validator("DistanceMetric")
    def validate_distance_metric(cls, value):
        assert value in [DOT_PRODUCT, EUCLIDEAN, COSINE]
        return value

    def __eq__(self, __value: object) -> bool:
        if id(__value)==id(self): #check if its a reference to the same object
            return True
        if not isinstance(__value, type(self)): #check if the objects are the same class
            return False
        if self.Text!=None or __value.Text!=None:
            if self.Text==__value.Text: #check if the objects have identical text
                return True
        if self.Embedding!=None and __value.Embedding !=None: #compare embeddings
            if self.DistanceMetric == EUCLIDEAN:
                distance=euclidean(self.Embedding, __value.Embedding)
            elif self.DistanceMetric == COSINE:
                distance= cosine(self.Embedding, __value.Embedding)
            elif self.DistanceMetric==DOT_PRODUCT:
                distance= np.dot(self.Embedding, __value.Embedding) * cosine(self.Embedding, __value.Embedding)
            if distance<= self.DistanceThreshold:
                return True
            else:
                return False
        return False
        
class TimeframeModel(BaseModel): #this can be anything that could have a start and/or end date and description
    Start: Optional[date]
    End: Optional[date]
    Description: Optional[DescriptionModel]

    def could_overlap(self, _timeframe_model)-> bool:
        if self.Start != None and self.End != None and _timeframe_model.Start != None and _timeframe_model.End != None:
            return self.End > _timeframe_model.Start and _timeframe_model.End >self.Start
        elif self.End != None and _timeframe_model.Start != None:
            return self.End > _timeframe_model.Start
        elif self.Start != None and _timeframe_model.End != None:
            return _timeframe_model.End > self.Start
        return True


class GeneralExperience(TimeframeModel): #this class will serve as both jobs and education
    Institution: Optional[str] #company/school
    InstitutionDescription: Optional[DescriptionModel]
    Specialization: Optional[str] #role/field of study
    SpecializationDescription: Optional[DescriptionModel]
    Tagline: Optional[DescriptionModel] #"job at company", "major at school"

    def __init__(self, Institution=None, Specialization=None, **kwargs):
        super().__init__(**kwargs)
        self.Institution=Institution
        self.Specialization=Specialization
        text=self.__str__()
        embedding= create_embedding(text)
        self.Tagline=DescriptionModel(Text=text, Embedding=embedding)
        if self.Institution!=None:
            self.InstitutionDescription=DescriptionModel(Text=self.Institution, Embedding=create_embedding(self.Institution))
        if self.Specialization!=None:
            self.SpecializationDescription=DescriptionModel(Text=self.Specialization, Embedding=create_embedding(self.Specialization))

    def __str__(self):
        if self.Institution!=None and self.Specialization!=None:
            return '{} at {}'.format(self.Specialization, self.Institution)
        elif self.Institution!=None:
            return self.Institution
        elif self.Specialization != None:
            return self.Specialization
        return ''

    def __eq__(self, __value: object) -> bool:
        if not self.could_overlap(__value): #if the timeframes cant match up then these are different things
            return False
        if self.Institution !=None and self.Specialization !=None and __value.Institution != None and __value.Specialization != None:
            return self.Tagline==__value.Tagline
        elif self.Institution !=None and __value.Instutution != None:
            return self.InstitutionDescription==__value.InstitutionDescription
        elif self.Specialization !=None and __value.Specialization != None:
            return self.SpecializationDescription==__value.SpecializationDesciption
        return True

class WorkExperience(GeneralExperience):
    def __str__(self):
        if self.Institution!=None and self.Specialization!=None:
            return 'this person worked as {} at company called {}'.format(self.Specialization, self.Institution)
        elif self.Institution!=None:
            return self.Institution
        elif self.Specialization != None:
            return self.Specialization
        return ''
    
class EducationExperience(GeneralExperience):
    def __str__(self):
        if self.Institution!=None and self.Specialization!=None:
            return 'this person studied {} at school called {}'.format(self.Specialization, self.Institution)
        elif self.Institution!=None:
            return self.Institution
        elif self.Specialization != None:
            return self.Specialization
        return ''

class Candidate:
    def __init__(self,
    Name: str,
    Location: str=None,
    Summary: DescriptionModel=None,
    Skills: List[str]=[],
    WorkExperienceList: List[WorkExperience]=[],
    EducationExperienceList: List[EducationExperience]=[],
    Tags: List[str]=[],
    Sources: List[str]=[]): #linkedin urls, github urls, stack overflow urls, etc
        self.Name=Name
        self.Location=Location
        self.Summary=Summary
        self.Skills=Skills
        self.WorkExperienceList=WorkExperienceList
        self.EducationExperienceList=EducationExperienceList
        self.Tags=Tags
        self.Sources=Sources
        if self.Summary==None or len(self.Summary.Text)==0:
            summary_text='this person is named {}'.format(Name)
            if  len(WorkExperienceList)>0:
                summary_text+=' '.join([str(work) for work in self.WorkExperienceList])
            if len(EducationExperienceList)>0:
                summary_text+=' '.join([str(edu) for edu in self.EducationExperienceList])
            if len(self.Skills)>0:
                summary_text+="this person is skilled in "+" and ".join([ski for ski in Skills])
            summary_embedding=create_embedding(summary_text)
            self.Summary=DescriptionModel(Text=summary_text, Embedding=summary_embedding)


    def __eq__(self, __value: object) -> bool:
        for src in self.Sources:
            for other_src in __value.Sources:
                if src==other_src:
                    return True #if two candidates link to one another then its the same person
        if self.Summary == __value.Summary:
            return True #if two candidates have super similar summaries then its probably the same person
        if self.Name==__value.Name:
            #if two candidates have the exact same name then its the same person
            #even similar names we don't want to unnecessarily match because sometimes common names are similar
            return True