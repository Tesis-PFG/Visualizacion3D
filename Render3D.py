import vtk

def load_dicom_images(dicom_dir):
    reader = vtk.vtkDICOMImageReader()
    reader.SetDirectoryName(dicom_dir)
    reader.Update()
    return reader

def extract_structure(dicom_reader, structure):
    threshold = vtk.vtkImageThreshold()
    threshold.SetInputConnection(dicom_reader.GetOutputPort())
    
    if structure == 'skin':
        threshold.ThresholdByLower(-100)
        threshold.ThresholdByUpper(20)
    elif structure == 'bone':
        threshold.ThresholdByLower(100)
    elif structure == 'brain':
        threshold.ThresholdByLower(50)
        threshold.ThresholdByUpper(60)
    
    threshold.ReplaceInOn()
    threshold.SetInValue(0)  # Background value
    threshold.ReplaceOutOn()
    threshold.SetOutValue(1)  # Foreground value (structure)

    marching_cubes = vtk.vtkMarchingCubes()
    marching_cubes.SetInputConnection(threshold.GetOutputPort())
    marching_cubes.SetValue(0, 1)
    
    smoother = vtk.vtkSmoothPolyDataFilter()
    smoother.SetInputConnection(marching_cubes.GetOutputPort())
    smoother.SetNumberOfIterations(30)
    smoother.SetRelaxationFactor(0.1)
    smoother.FeatureEdgeSmoothingOff()
    smoother.BoundarySmoothingOn()
    smoother.Update()

    return smoother

def create_render_window(surface):
    surface_mapper = vtk.vtkPolyDataMapper()
    surface_mapper.SetInputConnection(surface.GetOutputPort())

    surface_actor = vtk.vtkActor()
    surface_actor.SetMapper(surface_mapper)

    renderer = vtk.vtkRenderer()
    renderer.AddActor(surface_actor)
    renderer.SetBackground(0.1, 0.2, 0.3)

    render_window = vtk.vtkRenderWindow()
    render_window.AddRenderer(renderer)

    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(render_window)

    return render_window, interactor

def render_dicom_structure(dicom_dir, structure):
    dicom_reader = load_dicom_images(dicom_dir)
    structure_surface = extract_structure(dicom_reader, structure)
    render_window, interactor = create_render_window(structure_surface)
    render_window.Render()
    interactor.Start()

if __name__ == "__main__":
    dicom_directory = "E:\Documents\OneDrive - Pontificia Universidad Javeriana\Trabajos_pontifarras\Octavo_Semestre\Tesis\Material Cecile\Code\Data\T1_3D_TFE_AXI_501"
    
    # Selecciona la estructura a visualizar: 'skin', 'bone', 'brain'
    structure_to_render = 'brain'
    render_dicom_structure(dicom_directory, structure_to_render)

