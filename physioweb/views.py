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
    """_summary_: Creates the View for the mRNA Section in the DashBoard

    Args:
        TemplateView (TemplateView): Class TemplateView

    """
    
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
        return [i[0] for i in gene_names]
        
    
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
            return self.draw_figure_from_trajectory(request, form)
        
        if request.POST["Gene"]:
            self.add_list.remove(request.POST["Gene"])
            if len(self.add_list) > 0:
                return self.draw_figure_from_trajectory(request, form)
            else:
                return render(request, self.template_name, {'form': form,
                                                    "gene_names": self.gene_names,
                                                    "genes_listed": self.add_list})

    # TODO Rename this here and in `post`
    def draw_figure_from_trajectory(self, request, form):
        trajectory_df = self.search_gene_database()
        fig = self.get_dataframe_figures(trajectory_df)
        return render(request, self.template_name, {'form': form,
                                                "gene_names": self.gene_names,
                                                "genes_listed": list(set(self.add_list)),
                                                "plot_cell":fig,
                                                "draw": True})
                
     
     
    def get_dataframe_figures(self, trajectory_df):
        """Get DataFrame 

        Args:
            trajectory_df (_type_): _description_

        Returns:
            _type_: _description_
        """
        ad3_traj = trajectory_df[trajectory_df["Cellline"] == "AD3"] # preselect the celline clone
        ad2_traj = trajectory_df[trajectory_df["Cellline"] == "AD2"]
        traj_840 = trajectory_df[trajectory_df["Cellline"] == "840"]
        
        fig_all = self.draw_altair_graph(trajectory_df, "Trajectory", 800, 300, "GeneName")
        fig_ad3 = self.draw_altair_graph(ad3_traj, "Trajectory",500,300, "GeneName")
        fig_ad2 = self.draw_altair_graph(ad2_traj, "Trajectory",500,300, "GeneName")
        fig_840 = self.draw_altair_graph(traj_840, "Trajectory",500,300, "GeneName")
        
        return (fig_ad3, fig_ad2, fig_840)
        
                
            
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
                                        labelColor = 'black').configure_axis(grid = True, 
                                                                        labelFontSize = 15,
                                                                        gridColor = "#3EB489",
                                                                        labelColor = "black").configure_view(strokeOpacity = 0)
                                        
        return final_plot.to_json()
          
     
    def search_gene_database(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        query_set = GeneMapHuman.objects.all().values('ensembl')
        
        # check that the gene is inside the selection list
        gene_symbols = query_set.filter(gene_symbol__in =self.add_list)
        gene_symbols_list = gene_symbols.values_list()
        gene_names = [i[1] for i in gene_symbols_list]

        query_set = self.database.objects.all().values()
        trajectory = query_set.filter(GeneName__in =gene_names)
        if trajectory_list := trajectory.values_list():
            return self.dictionary_gene_trajectories(trajectory_list)
        
    
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
        return pd.DataFrame(trajectory_dict)
    
class HomeView(TemplateView):
    """_summary_: This creates the view for the Index Page

    Args:
        TemplateView (TemplateView): _description_
    """
    template_name = "index.html"
    
    
class EphysDash(TemplateView):
    """_summary_

    Args:
        TemplateView (_type_): _description_
    """
    print("returns the ephys dashboard")
    template_name = "ephys_dashbord.html"
    description_temp = {
        "description":"description_biophys.html"
    }
    template_desc = None
    
    def get(self, request, *args, **kwargs):
        
        render_desc = False
        if request.GET.get("name"):
            print("yeah here we are")
            self.template_desc = self.description_temp.get(request.GET.get("name"))
            render_desc = True
        return render(request, self.template_name, {"template_docu":self.template_desc,
                                                    "render_temp": render_desc,
                                                    "title":request.GET.get("name")})
    

    
    
