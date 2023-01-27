from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from physioweb.forms import GeneName
from .models import *
import pandas as pd
import altair as alt
from altair.utils.display import HTMLRenderer
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token
from django.template.loader import render_to_string
import scipy.stats as stats


class DashBoardView(TemplateView):
    """Dashboard for the Data of the mRNA transcriptomics

    Args:
        TemplateView (_type_): _description_
    """
    template_name = "dashboard.html"


class mRNAView(TemplateView):
    
    template_name = "dashboard.html"
    success_url = '/mRNA'
    form_class = GeneName
    add_list = []
    gene_names = []
    database = IpscMrna
    columns = [9* [i] for i in ["Day00","Day05","Day09","Day16","Day26","Day36"]]
    columns = [t for i in columns for t in i]
    cellline = [3*[i] for i in ["AD3","AD2","840"]]*6
    cellline = [t for i in cellline for t in i]
    

    def get(self, request, *args, **kwargs):
        """Reacts to the Get request from the mRNA Webpage renders the form for interactive
        mRNA visualizations

        Args:
            request (request): Get Request after button click on mRNA transcriptomcis

        Returns:
            render: The mRNA template with the form (input gene) and the genes_list for autosuggestions
        """
        form = self.form_class
        print(form.errors)
        gene_names = self.get_genes()
        self.gene_names.extend(gene_names)
        
        return render(request, self.template_name, {'form': form,
                                                    "gene_names": self.gene_names,
                                                    "genes_listed": self.add_list})
        
    def get_genes(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        gene_names= GeneMapHuman.objects.values_list("gene_symbol")
        gene_names = list(gene_names)
        gene_names = [i[0] for i in gene_names]
        return gene_names
        
    
    def post(self, request, *args, **kwargs):
        """Post Request 

        Args:
            request (_type_): 

        Returns:
            _type_: _description_
        """
        form = self.form_class
        form_value = self.form_class(request.POST)    
        
        if form_value.is_valid():
            gene = form_value.cleaned_data["gene_name"].split(" ")
            self.add_list.extend(gene)
            trajectory_df = self.search_gene_database()
            fig = self.get_dataframe_figures(trajectory_df)
            return render(request, self.template_name, {'form': form,
                                                    "gene_names": self.gene_names,
                                                    "genes_listed": self.add_list,
                                                    "plot": fig[0],
                                                    "plot_cell":fig[1:],
                                                    "draw": True})
            
        if request.POST["Gene"]:
            self.add_list.remove(request.POST["Gene"])
            if len(self.add_list) > 0:
                trajectory_df = self.search_gene_database()
                fig = self.get_dataframe_figures(trajectory_df)
                return render(request, self.template_name, {'form': form,
                                                        "gene_names": self.gene_names,
                                                        "genes_listed": self.add_list,
                                                        "plot": fig[0],
                                                        "plot_cell":fig[1:],
                                                        "draw": True})
            else:
                return render(request, self.template_name, {'form': form,
                                                    "gene_names": self.gene_names,
                                                    "genes_listed": self.add_list})
                
     
     
    def get_dataframe_figures(self, trajectory_df):
        """Get DataFrame 

        Args:
            trajectory_df (_type_): _description_

        Returns:
            _type_: _description_
        """
        ad3_traj = trajectory_df[trajectory_df["Cellline"] == "AD3"]
        ad2_traj = trajectory_df[trajectory_df["Cellline"] == "AD2"]
        traj_840 = trajectory_df[trajectory_df["Cellline"] == "840"]
        fig_all = self.draw_altair_graph(trajectory_df, "Trajectory", 800, 300, "GeneName")
        fig_ad3 = self.draw_altair_graph(ad3_traj, "Trajectory",500,300, "GeneName")
        fig_ad2 = self.draw_altair_graph(ad2_traj, "Trajectory",500,300, "GeneName")
        fig_840 = self.draw_altair_graph(traj_840, "Trajectory",500,300, "GeneName")
        
        return (fig_all, fig_ad3, fig_ad2, fig_840)
        
                
            
    def draw_altair_graph(self,data_draw, value, width, height,  gene_annotation = None):
        """ Draws the trajectories as altair graph
        Args:
            data_draw: pd.DataFrame -> preselected data of genes
            value: str -> should be the column that holds the normalized data
            gene_annotation: str -> columns that is holding the hue
        """ 
        #selection = alt.selection_multi(fields=[gene_annotation], bind='legend')
        chart = (
                    alt.Chart(data_draw)
                    .mark_boxplot(size = 30)
                    .encode(x=alt.X("Timepoint"),
                            y=alt.Y(value, scale=alt.Scale(domain=[data_draw[value].min()-1, data_draw[value].max()+1])),
                            color=gene_annotation,
                            )
                    .properties(width=width, height = height)
                    )
            
        chart_line = (
                alt.Chart(data_draw)
                .mark_line(interpolate = "natural")
                .encode(x=alt.X("Timepoint",
                                scale=alt.Scale(padding=1)),
                                y=alt.Y(f"mean({value})",scale=alt.Scale(domain=[data_draw[value].min()-1, data_draw[value].max()+1])),
                                color=gene_annotation,
                                )
                .properties(width=width, height = height)
        )
                       
        final_plot = chart_line + chart
        final_plot  = final_plot.configure(background="transparent").configure_legend(padding=2,
                                        cornerRadius=5,
                                        orient='bottom',
                                        labelColor = 'white').configure_axis(grid = False, 
                                                                        labelFontSize = 15,
                                                                        gridColor = "#3EB489",
                                                                        labelColor = "white").configure_view(strokeOpacity = 0)
                                        
        return final_plot.to_json()
          
     
    def search_gene_database(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        query_set = GeneMapHuman.objects.all().values('ensembl')
        gene_symbols = query_set.filter(gene_symbol__in =self.add_list)
        gene_symbols_list = gene_symbols.values_list()
        gene_names = [i[1] for i in gene_symbols_list]
        
        query_set = self.database.objects.all().values()
        trajectory = query_set.filter(GeneName__in =gene_names)
        trajectory_list = trajectory.values_list()
        
        if trajectory_list:
            trajectory_df = self.dictionary_gene_trajectories(trajectory_list)
            return trajectory_df
        
    
    def dictionary_gene_trajectories(self, trajectories):
        """Put trajectories into readable dataframe for plotting
        
        Args:
            trajectories (list): List of tuples derived from the iPSC database
        """
        trajectory_dict = {"Timepoint":[], "GeneName" : [], "Trajectory":[], "Cellline": []}
        for gene in trajectories:
            trajectory_dict["GeneName"].extend([gene[1]] * len(self.columns))
            trajectory_dict["Timepoint"].extend(self.columns)
            trajectory_dict["Trajectory"].extend(stats.zscore(gene[2:]))
            trajectory_dict["Cellline"].extend(self.cellline)
        trajectory_df = pd.DataFrame(trajectory_dict)
        return trajectory_df
    
class HomeView(TemplateView):
    """_summary_

    Args:
        TemplateView (_type_): _description_
    """
    template_name = "index.html"
    

    
    
