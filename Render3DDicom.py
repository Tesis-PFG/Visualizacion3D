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
    elif structure == 'bone_and_electrodes':
        threshold.ThresholdByLower(0)
        threshold.ThresholdByUpper(10)

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

def create_color_transfer_function():
    color_transfer_function = vtk.vtkColorTransferFunction()

   # Asignar colores a valores escalares específicos
    color_transfer_function.AddRGBPoint(28.5064, 0.188235, 0.188235, 0.0705882) # Value = 28.5064
    color_transfer_function.AddRGBPoint(33.7963, 0.690196, 0.12549, 0.0627451)  # Value = 33.7963
    color_transfer_function.AddRGBPoint(50.9885, 0.741176, 0.184314, 0.0745098) # Value = 50.9885
    color_transfer_function.AddRGBPoint(56.2784, 0.831373, 0.266667, 0.0941176) # Value = 56.2784
    color_transfer_function.AddRGBPoint(450.376, 0.831373, 0.411765, 0.133333)  # Value = 450.376
    
    return color_transfer_function

def create_opacity_transfer_function():
    opacity_function = vtk.vtkPiecewiseFunction()

# Valores de opacidad en diferentes niveles
    opacity_function.AddPoint(0, 0.0)            # Value = 0
    opacity_function.AddPoint(81.8865, 0.477679) # Value = 81.8865
    opacity_function.AddPoint(234.365, 1.0)      # Value = 234.365
    opacity_function.AddPoint(450.376, 1.0)      # Value = 450.376


    return opacity_function

def create_render_window(surface, color_function, opacity_function):
    surface_mapper = vtk.vtkPolyDataMapper()
    surface_mapper.SetInputConnection(surface.GetOutputPort())
    surface_mapper.SetLookupTable(color_function)
    surface_mapper.SetScalarRange(0, 5)

    surface_actor = vtk.vtkActor()
    surface_actor.SetMapper(surface_mapper)

    renderer = vtk.vtkRenderer()
    renderer.AddVolume(surface_actor)
    renderer.SetBackground(0.1, 0.2, 0.3)

    render_window = vtk.vtkRenderWindow()
    render_window.AddRenderer(renderer)

    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(render_window)

    # Configurar el estilo de interacción para arrastrar el modelo con el mouse
    style = vtk.vtkInteractorStyleTrackballCamera()
    interactor.SetInteractorStyle(style)

    return render_window, interactor

def render_dicom_structure(dicom_dir, structure):
    dicom_reader = load_dicom_images(dicom_dir)
    structure_surface = extract_structure(dicom_reader, structure)
    
    # Create lookup table for coloring
    lookup_table = create_color_transfer_function()
    opacity_function = create_opacity_transfer_function()
    
    render_window, interactor = create_render_window(structure_surface, lookup_table, opacity_function)
    render_window.Render()
    interactor.Start()

if __name__ == "__main__":
    dicom_directory = "E:/Documents/OneDrive - Pontificia Universidad Javeriana/Trabajos_pontifarras/Octavo_Semestre/Tesis/Codigo/CodigoBase/Data/reg/RM/T1_3D_TFE_AXI_501"
    
    # Selecciona la estructura a visualizar: 'skin', 'bone', 'brain', 'bone_and_electrodes'
    structure_to_render = 'bone_and_electrodes'
    render_dicom_structure(dicom_directory, structure_to_render)
