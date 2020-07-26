
/**
 * @author ericyjw
 */

import java.awt.*;
import java.io.File;
import java.io.IOException;

import org.gephi.appearance.api.AppearanceController;
import org.gephi.appearance.api.AppearanceModel;
import org.gephi.appearance.api.Function;
import org.gephi.appearance.api.Partition;
import org.gephi.appearance.api.PartitionFunction;
import org.gephi.appearance.plugin.PartitionElementColorTransformer;
import org.gephi.appearance.plugin.RankingNodeSizeTransformer;
import org.gephi.appearance.plugin.palette.Palette;
import org.gephi.appearance.plugin.palette.PaletteManager;
import org.gephi.filters.api.Range;
import org.gephi.filters.plugin.edge.EdgeWeightBuilder.EdgeWeightFilter;
import org.gephi.filters.plugin.operator.NOTBuilderEdge.NotOperatorEdge;
import org.gephi.filters.spi.Filter;
import org.gephi.graph.api.Column;
import org.gephi.graph.api.DirectedGraph;
import org.gephi.graph.api.GraphController;
import org.gephi.graph.api.GraphModel;
import org.gephi.io.exporter.api.ExportController;
import org.gephi.io.exporter.plugin.ExporterSpreadsheet;
import org.gephi.io.exporter.spi.GraphExporter;
import org.gephi.io.exporter.spi.GraphFileExporterBuilder;
import org.gephi.io.importer.api.Container;
import org.gephi.io.importer.api.EdgeDirectionDefault;
import org.gephi.io.importer.api.ImportController;
import org.gephi.io.importer.impl.ImportControllerImpl;
import org.gephi.io.processor.plugin.DefaultProcessor;
import org.gephi.layout.plugin.force.StepDisplacement;
import org.gephi.layout.plugin.force.yifanHu.YifanHuLayout;
import org.gephi.layout.plugin.forceAtlas.ForceAtlasLayout;
import org.gephi.layout.plugin.forceAtlas2.ForceAtlas2;
import org.gephi.layout.plugin.labelAdjust.LabelAdjust;
import org.gephi.layout.plugin.noverlap.NoverlapLayout;
import org.gephi.preview.api.PreviewController;
import org.gephi.preview.api.PreviewModel;
import org.gephi.preview.api.PreviewProperty;
import org.gephi.project.api.ProjectController;
import org.gephi.project.api.Workspace;
import org.gephi.statistics.plugin.Modularity;
import org.gephi.statistics.plugin.WeightedDegree;
import org.openide.util.Lookup;

public class Main {

    public static void main(String[] args) {
        String savingDir = args[0];
        System.out.println("Saving to: " + savingDir);

        // Init a project - and therefore a workspace
        ProjectController pc = Lookup.getDefault().lookup(ProjectController.class);
        pc.newProject();
        Workspace workspace = pc.getCurrentWorkspace();

        // Get controllers and models
        ImportController importController = Lookup.getDefault().lookup(ImportController.class);
        GraphModel graphModel = Lookup.getDefault().lookup(GraphController.class).getGraphModel();
        PreviewModel model = Lookup.getDefault().lookup(PreviewController.class).getModel();
        AppearanceController appearanceController = Lookup.getDefault().lookup(AppearanceController.class);
        AppearanceModel appearanceModel = Lookup.getDefault().lookup(AppearanceController.class).getModel();

        ImportControllerImpl importController1 = Lookup.getDefault().lookup(ImportControllerImpl.class);
        // Import file
        Container container;
        try {
            String filename = args[1];
            System.out.println("Processing file: " + filename);
            File file = new File(filename);

            container = importController.importFile(file);

            container.getLoader().setEdgeDefault(EdgeDirectionDefault.UNDIRECTED);
            container.getLoader().setAllowAutoNode(true);
            container.getLoader().setAllowSelfLoop(true);
            container.getLoader().setAutoScale(true);
        } catch (Exception ex) {
            ex.printStackTrace();
            return;
        }

        // Append imported data to GraphAPI
        importController.process(container, new DefaultProcessor(), workspace);

        /* ===== Filtering ===== */
        DirectedGraph graph = filterOutLowCorr(graphModel);

        /* ===== Preview ===== */
        identifyClusters(graphModel, appearanceController, appearanceModel, graph);

        resizeNodeSizesByWeightedDegree(graphModel, appearanceController, appearanceModel, graph);

        model.getProperties().putValue(PreviewProperty.SHOW_NODE_LABELS, true);
        model.getProperties().putValue(PreviewProperty.EDGE_THICKNESS, 0.1f);
        model.getProperties().putValue(PreviewProperty.EDGE_CURVED, false);
        model.getProperties().putValue(PreviewProperty.NODE_LABEL_PROPORTIONAL_SIZE, true);

        /* ===== Layout ===== */
        applyYifanHuLayout(graphModel);

        applyForceAtlasLayout(graphModel);

        applyForceAtlas2Layout(graphModel);

        applyNoOverlapLayout(graphModel);

        applyLabelAdjustLayout(graphModel);

        /* ===== Export ===== */
        // Export full graph
        ExportController ec = Lookup.getDefault().lookup(ExportController.class);
        String file = args[1].substring(0, args[1].length() - 4);
        String[] filename = file.split("/");
        String export_filename = filename[filename.length - 1] + "_network";

        try {
            File directory = new File(savingDir + "/png/");
            if (!directory.exists()) directory.mkdirs();

            ec.exportFile(new File(savingDir + "/png/" + export_filename + ".png"));

            directory = new File(savingDir + "/pdf/");
            if (!directory.exists()) directory.mkdirs();
            ec.exportFile(new File(savingDir + "/pdf/" + export_filename + ".pdf"));

            directory = new File(savingDir + "/svg/");
            if (!directory.exists()) directory.mkdirs();
            ec.exportFile(new File(savingDir + "/svg/" + export_filename + ".svg"));

        } catch (IOException ex) {
            ex.printStackTrace();
        }

        File directory = new File(savingDir);
        if (!directory.exists()) directory.mkdirs();

        ExporterSpreadsheet.ExportTable currentTable = ExporterSpreadsheet.ExportTable.NODES;

        for (GraphFileExporterBuilder builder : Lookup.getDefault().lookupAll(GraphFileExporterBuilder.class)) {

            if (builder.getName().toLowerCase().startsWith("spreadsheet")) {
                GraphExporter exporter = builder.buildExporter();
                ((ExporterSpreadsheet) exporter).setTableToExport(currentTable);
                try {
                    directory = new File(savingDir + "/csv/");
                    if (!directory.exists()) directory.mkdirs();

                    ec.exportFile(new File(savingDir + "/csv/" + export_filename + ".csv"),exporter);
                } catch (IOException ex) {
                    ex.printStackTrace();
                    return;
                }
            }
        }

    }

    private static void resizeNodeSizesByWeightedDegree(GraphModel graphModel,
                                                        AppearanceController appearanceController,
                                                        AppearanceModel appearanceModel, DirectedGraph graph) {
        WeightedDegree degree = new WeightedDegree();
        degree.execute(graph);

        Column degreeCol = graphModel.getNodeTable().getColumn(WeightedDegree.WDEGREE);
        Function rankingSizeNodeFunc = appearanceModel.getNodeFunction(graph, degreeCol,
            RankingNodeSizeTransformer.class);
        RankingNodeSizeTransformer rankingNodeSizeTransformer = rankingSizeNodeFunc.getTransformer();
        rankingNodeSizeTransformer.setMinSize(5);
        rankingNodeSizeTransformer.setMaxSize(15);
        appearanceController.transform(rankingSizeNodeFunc);
    }

    private static void identifyClusters(GraphModel graphModel, AppearanceController appearanceController,
                                         AppearanceModel appearanceModel, DirectedGraph graph) {
        Modularity modularity = new Modularity();
        modularity.execute(graph);

        Column modColumn = graphModel.getNodeTable().getColumn(Modularity.MODULARITY_CLASS);
        Function func = appearanceModel.getNodeFunction(graph, modColumn, PartitionElementColorTransformer.class);
        Partition partition = ((PartitionFunction) func).getPartition();
        System.out.println(partition.size() + " partitions found");

        Palette palette;
        if (partition.size() <= 5) {
            Color[] preset = new Color[]{new Color(0x4788FF), new Color(0xFF3F29), new Color(0x3BFF9A),
                new Color(0x42EFFF), new Color(0xFFC951)};
            Color[] chosen = new Color[partition.size()];
            System.arraycopy(preset, 0, chosen, 0, partition.size());
            palette = new Palette(chosen);
        } else {
            palette = PaletteManager.getInstance().generatePalette(partition.size());
        }
        partition.setColors(palette.getColors());
        appearanceController.transform(func);
    }

    // Filter, filter degree between -0.2 and 0.2
    private static DirectedGraph filterOutLowCorr(GraphModel graphModel) {
        EdgeWeightFilter corrFilter = new EdgeWeightFilter();
        corrFilter.init(graphModel.getGraph());
        corrFilter.setRange(new Range(-0.4, 0.4));

        NotOperatorEdge notOperatorFilter = new NotOperatorEdge();
        notOperatorFilter.filter(graphModel.getGraph(), new Filter[]{corrFilter});

        DirectedGraph graph = graphModel.getDirectedGraphVisible();
        System.out.println("Nodes: " + graph.getNodeCount() + " Edges: " + graph.getEdgeCount());
        return graph;
    }

    private static void applyLabelAdjustLayout(GraphModel graphModel) {
        LabelAdjust labelAdjustLayout = new LabelAdjust(null);
        labelAdjustLayout.setGraphModel(graphModel);
        labelAdjustLayout.resetPropertiesValues();
        labelAdjustLayout.initAlgo();
        for (int i = 0; i < 100 && labelAdjustLayout.canAlgo(); i++) {
            labelAdjustLayout.goAlgo();
        }
        labelAdjustLayout.endAlgo();
    }

    private static void applyNoOverlapLayout(GraphModel graphModel) {
        NoverlapLayout noOverlapLayout = new NoverlapLayout(null);
        noOverlapLayout.setGraphModel(graphModel);
        noOverlapLayout.resetPropertiesValues();
        noOverlapLayout.initAlgo();
        for (int i = 0; i < 10 && noOverlapLayout.canAlgo(); i++) {
            noOverlapLayout.goAlgo();
        }
        noOverlapLayout.endAlgo();
    }

    private static void applyForceAtlas2Layout(GraphModel graphModel) {
        ForceAtlas2 forceAtlas2Layout = new ForceAtlas2(null);
        forceAtlas2Layout.setGraphModel(graphModel);
        forceAtlas2Layout.resetPropertiesValues();
        forceAtlas2Layout.setLinLogMode(true);
        forceAtlas2Layout.setOutboundAttractionDistribution(true);

        forceAtlas2Layout.initAlgo();
        for (int i = 0; i < 10 && forceAtlas2Layout.canAlgo(); i++) {
            forceAtlas2Layout.goAlgo();
        }
        forceAtlas2Layout.endAlgo();
    }

    private static void applyForceAtlasLayout(GraphModel graphModel) {
        ForceAtlasLayout forceAtlasLayout = new ForceAtlasLayout(null);
        forceAtlasLayout.setGraphModel(graphModel);
        forceAtlasLayout.resetPropertiesValues();
        forceAtlasLayout.setAdjustSizes(true);

        forceAtlasLayout.initAlgo();
        for (int i = 0; i < 100 && forceAtlasLayout.canAlgo(); i++) {
            forceAtlasLayout.goAlgo();
        }
        forceAtlasLayout.endAlgo();
    }

    private static void applyYifanHuLayout(GraphModel graphModel) {
        YifanHuLayout yifanHuLayout = new YifanHuLayout(null, new StepDisplacement(1f));
        yifanHuLayout.setGraphModel(graphModel);
        yifanHuLayout.resetPropertiesValues();
        yifanHuLayout.setOptimalDistance(200f);

        yifanHuLayout.initAlgo();
        for (int i = 0; i < 100 && yifanHuLayout.canAlgo(); i++) {
            yifanHuLayout.goAlgo();
        }
        yifanHuLayout.endAlgo();
    }
}
