import vtk

def load_mhd_image(mhd_file):
    reader = vtk.vtkMetaImageReader()
    reader.SetFileName(mhd_file)
    reader.Update()
    return reader

def extract_structure(image_reader, structure):
    threshold = vtk.vtkImageThreshold()
    threshold.SetInputConnection(image_reader.GetOutputPort())

    if structure == 'skin':
        threshold.ThresholdByLower(-100)
        threshold.ThresholdByUpper(20)
    elif structure == 'bone':
        threshold.ThresholdByLower(100)
    elif structure == 'brain':
        threshold.ThresholdByLower(50)
        threshold.ThresholdByUpper(60)
    elif structure == 'bone_and_electrodes':
        threshold.ThresholdByLower(50)
        threshold.ThresholdByUpper(150)

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
    color_transfer_function.AddRGBPoint(0, 0.878431, 0.301961, 0.301961)      # Value = 0
    color_transfer_function.AddRGBPoint(66.3563, 0.419608, 0.0, 0.0)          # Value = 66.3563
    color_transfer_function.AddRGBPoint(97.4167, 1.0, 0.380392, 0.0)          # Value = 97.4167
    color_transfer_function.AddRGBPoint(168.008, 1.0, 1.0, 0.0)               # Value = 168.008
    color_transfer_function.AddRGBPoint(186.362, 0.0, 0.501961, 1.0)          # Value = 186.362
    color_transfer_function.AddRGBPoint(196.245, 1.0, 1.0, 1.0)               # Value = 196.245
    color_transfer_function.AddRGBPoint(208.952, 0.0, 0.360784, 1.0)          # Value = 208.952
    color_transfer_function.AddRGBPoint(450.376, 0.278431, 0.278431, 0.858824)# Value = 450.376

    return color_transfer_function

def create_opacity_transfer_function():
    opacity_function = vtk.vtkPiecewiseFunction()

    # Valores de opacidad en diferentes niveles
    opacity_function.AddPoint(0, 0.0)      
    opacity_function.AddPoint(22.5894, 0.0)       
    opacity_function.AddPoint(69.1799, 0.0)       
    opacity_function.AddPoint(88.9456, 0.53125)              
    opacity_function.AddPoint(93.1812, 0.0)  
    opacity_function.AddPoint(127.065, 0.0)  
    opacity_function.AddPoint(196.245, 0.0)  
    opacity_function.AddPoint(266.837, 0.901786) 

    return opacity_function

def create_render_window(volume_mapper, color_function, opacity_function):
    volume_property = vtk.vtkVolumeProperty()
    volume_property.SetColor(color_function)
    volume_property.SetScalarOpacity(opacity_function)
    volume_property.ShadeOn()  # Activar sombreado para un efecto más realista
    volume_property.SetInterpolationTypeToLinear()

    volume = vtk.vtkVolume()
    volume.SetMapper(volume_mapper)
    volume.SetProperty(volume_property)

    renderer = vtk.vtkRenderer()
    renderer.AddVolume(volume)
    renderer.SetBackground(0.1, 0.2, 0.3)

    render_window = vtk.vtkRenderWindow()
    render_window.AddRenderer(renderer)

    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(render_window)

    # Configurar el estilo de interacción para arrastrar el modelo con el mouse
    style = vtk.vtkInteractorStyleTrackballCamera()
    interactor.SetInteractorStyle(style)

    return render_window, interactor

def render_mhd_structure(mhd_file, structure):
    image_reader = load_mhd_image(mhd_file)

    volume_mapper = vtk.vtkGPUVolumeRayCastMapper()
    volume_mapper.SetInputConnection(image_reader.GetOutputPort())

    color_function = create_color_transfer_function()
    opacity_function = create_opacity_transfer_function()

    render_window, interactor = create_render_window(volume_mapper, color_function, opacity_function)
    render_window.Render()
    interactor.Start()

if __name__ == "__main__":
    mhd_file = "E:\Documents\OneDrive - Pontificia Universidad Javeriana\Trabajos_pontifarras\Octavo_Semestre\Tesis\Codigo\CodigoBase\Data\Eraw\patient.mhd"
    
    # Selecciona la estructura a visualizar: 'skin', 'bone', 'brain', 'bone_and_electrodes'
    structure_to_render = 'bone_and_electrodes'
    render_mhd_structure(mhd_file, structure_to_render)


