from django.db import models

# Create your models here.
class User(models.Model):
    """_summary_

    Args:
        models (_type_): _description_

    Returns:
        _type_: _description_
    """
    user = models.CharField(max_length=200)
    password = models.CharField(max_length=50)
    
    def __str__(self):
        return self.user
    
class GeneMapHuman(models.Model):
    """Create the database model to map genes and ensembl IDs for human

    Args:
        models (model): Database Model Django
    """
    ensembl = models.CharField(max_length= 200)
    gene_symbol = models.CharField(max_length=200)
    biotype = models.CharField(max_length=200)
    
    def __str__(self):
        return self.ensembl
    

class IpscMrna(models.Model):
    """_summary_

    Args:
        models (_type_): _description_
    """
    GeneName = models.CharField(max_length=100)
    sample_01 = models.FloatField()
    sample_02 = models.FloatField()
    sample_03 = models.FloatField()
    sample_04 = models.FloatField()
    sample_05 = models.FloatField()
    sample_06 = models.FloatField()
    sample_07 = models.FloatField()
    sample_08 = models.FloatField()
    sample_09 = models.FloatField()
    sample_10 = models.FloatField()
    sample_11 = models.FloatField()
    sample_12 = models.FloatField()
    sample_13 = models.FloatField()
    sample_14 = models.FloatField()
    sample_15 = models.FloatField()
    sample_16 = models.FloatField()
    sample_17 = models.FloatField()
    sample_18 = models.FloatField()
    sample_19 = models.FloatField()
    sample_20 = models.FloatField()
    sample_21 = models.FloatField()
    sample_22 = models.FloatField()
    sample_23 = models.FloatField()
    sample_24 = models.FloatField()
    sample_25 = models.FloatField()
    sample_26 = models.FloatField()
    sample_27 = models.FloatField()
    sample_28 = models.FloatField()
    sample_29 = models.FloatField()
    sample_30 = models.FloatField()
    sample_31 = models.FloatField()
    sample_32 = models.FloatField()
    sample_33 = models.FloatField()
    sample_34 = models.FloatField()
    sample_35 = models.FloatField()
    sample_36 = models.FloatField()
    sample_37 = models.FloatField()
    sample_38 = models.FloatField()
    sample_39 = models.FloatField()
    sample_40 = models.FloatField()
    sample_41 = models.FloatField()
    sample_42 = models.FloatField()
    sample_43 = models.FloatField()
    sample_44 = models.FloatField()
    sample_45 = models.FloatField()
    sample_46 = models.FloatField()
    sample_47 = models.FloatField()
    sample_48 = models.FloatField()
    sample_49 = models.FloatField()
    sample_50 = models.FloatField()
    sample_51 = models.FloatField()
    sample_52 = models.FloatField()
    sample_53 = models.FloatField()
    sample_54 = models.FloatField()
    
    def load_data(self, row):
        print()
        
class EphysTable(models.Model):
    user_1 = models.CharField(max_length = 200)