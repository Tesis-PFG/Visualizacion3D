import vtk

def load_mhd_image(mhd_file):
    reader = vtk.vtkMetaImageReader()
    reader.SetFileName(mhd_file)
    reader.Update()
    return reader

def extract_structure(image_reader, structure):
    threshold = vtk.vtkImageThreshold()
    threshold.SetInputConnection(image_reader.GetOutputPort())

    if structure == '1':
        threshold.ThresholdByLower(20)
        threshold.ThresholdByUpper(460)
    elif structure == '2':
        threshold.ThresholdByLower(40)
        threshold.ThresholdByUpper(245)
    elif structure == '3':
        threshold.ThresholdByLower(0)
        threshold.ThresholdByUpper(450)
    elif structure == '4':
        threshold.ThresholdByLower(196)
        threshold.ThresholdByUpper(456)
    

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

def create_color_transfer_function(structure):
    color_transfer_function = vtk.vtkColorTransferFunction()
    
    if structure == 1:  # Everything
        # Asignar colores a valores escalares específicos
        color_transfer_function.AddRGBPoint(28.5064, 0.188235, 0.188235, 0.0705882) # Value = 28.5064
        color_transfer_function.AddRGBPoint(33.7963, 0.690196, 0.12549, 0.0627451)  # Value = 33.7963
        color_transfer_function.AddRGBPoint(50.9885, 0.741176, 0.184314, 0.0745098) # Value = 50.9885
        color_transfer_function.AddRGBPoint(56.2784, 0.831373, 0.266667, 0.0941176) # Value = 56.2784
        color_transfer_function.AddRGBPoint(450.376, 0.831373, 0.411765, 0.133333)  # Value = 450.376
        
    elif structure == 2:  # Everything (alt)
        # Asignar colores a valores escalares específicos
        color_transfer_function.AddRGBPoint(40.0, 0.831373, 0.909804, 0.980392)   # Value = 40.0
        color_transfer_function.AddRGBPoint(42.5625, 0.74902, 0.862745, 0.960784) # Value = 42.5625
        color_transfer_function.AddRGBPoint(45.125, 0.694118, 0.827451, 0.941176) # Value = 45.125
        color_transfer_function.AddRGBPoint(50.25, 0.568627, 0.760784, 0.921569)  # Value = 50.25
        color_transfer_function.AddRGBPoint(55.375, 0.45098, 0.705882, 0.901961)  # Value = 55.375
        color_transfer_function.AddRGBPoint(60.5, 0.345098, 0.643137, 0.858824)   # Value = 60.5
        color_transfer_function.AddRGBPoint(65.625, 0.247059, 0.572549, 0.819608) # Value = 65.625
        color_transfer_function.AddRGBPoint(70.75, 0.180392, 0.521569, 0.780392)  # Value = 70.75
        color_transfer_function.AddRGBPoint(72.8, 0.129412, 0.447059, 0.74902)    # Value = 72.8
        color_transfer_function.AddRGBPoint(76.9, 0.129412, 0.447059, 0.709804)   # Value = 76.9
        
    elif structure == 3: #Electrodes and brain
        # Asignar colores a valores escalares específicos
        color_transfer_function.AddRGBPoint(0, 0.878431, 0.301961, 0.301961)      # Value = 0
        color_transfer_function.AddRGBPoint(66.3563, 0.419608, 0.0, 0.0)          # Value = 66.3563
        color_transfer_function.AddRGBPoint(97.4167, 1.0, 0.380392, 0.0)          # Value = 97.4167
        color_transfer_function.AddRGBPoint(168.008, 1.0, 1.0, 0.0)               # Value = 168.008
        color_transfer_function.AddRGBPoint(186.362, 0.0, 0.501961, 1.0)          # Value = 186.362
        color_transfer_function.AddRGBPoint(196.245, 1.0, 1.0, 1.0)               # Value = 196.245
        color_transfer_function.AddRGBPoint(208.952, 0.0, 0.360784, 1.0)          # Value = 208.952
        color_transfer_function.AddRGBPoint(450.376, 0.278431, 0.278431, 0.858824)# Value = 450.376
        
    elif structure == 4:  # Electrodes
        color_transfer_function.AddRGBPoint(196.0, 0.301961, 0.047059, 0.090196)    # Value = 196.0
        color_transfer_function.AddRGBPoint(200.169, 0.396078, 0.0392157, 0.0588235) # Value = 200.169
        color_transfer_function.AddRGBPoint(204.339, 0.494118, 0.054902, 0.0352941) # Value = 204.339
        color_transfer_function.AddRGBPoint(208.508, 0.588235, 0.113725, 0.0235294) # Value = 208.508
        color_transfer_function.AddRGBPoint(212.677, 0.662745, 0.168627, 0.0156863) # Value = 212.677
        color_transfer_function.AddRGBPoint(216.846, 0.741176, 0.227451, 0.00392157)# Value = 216.846
        color_transfer_function.AddRGBPoint(221.016, 0.788235, 0.290196, 0.0)       # Value = 221.016
        color_transfer_function.AddRGBPoint(225.185, 0.862745, 0.380392, 0.0117647) # Value = 225.185
        color_transfer_function.AddRGBPoint(229.354, 0.917647, 0.458824, 0.0470588) # Value = 229.354
        color_transfer_function.AddRGBPoint(233.524, 0.917647, 0.521569, 0.0470588) # Value = 233.524
    
    return color_transfer_function

def create_opacity_transfer_function(structure):
    opacity_function = vtk.vtkPiecewiseFunction()
    
    if structure == 1:  # Everything
        # Valores de opacidad en diferentes niveles
        opacity_function.AddPoint(0, 0.0)            # Value = 0
        opacity_function.AddPoint(81.8865, 0.477679) # Value = 81.8865
        opacity_function.AddPoint(234.365, 1.0)      # Value = 234.365
        opacity_function.AddPoint(450.376, 1.0)      # Value = 450.376
        
    elif structure == 2:  # Everything (alt)
        # Valores de opacidad en diferentes niveles
        opacity_function.AddPoint(40.0, 0.0)       # Value = 40.0
        opacity_function.AddPoint(245.0, 1.0)      # Value = 245.0

    elif structure == 3: #Electrodes and brain
        # Valores de opacidad en diferentes niveles
        opacity_function.AddPoint(0, 0.0)      
        opacity_function.AddPoint(22.5894, 0.0)       
        opacity_function.AddPoint(69.1799, 0.0)       
        opacity_function.AddPoint(88.9456, 0.53125)              
        opacity_function.AddPoint(93.1812, 0.0)  
        opacity_function.AddPoint(127.065, 0.0)  
        opacity_function.AddPoint(196.245, 0.0)  
        opacity_function.AddPoint(266.837, 0.901786) 
        
    elif structure == 4:  # Electrodes
        opacity_function.AddPoint(196.0, 0.0)      # Value = 196.0
        opacity_function.AddPoint(245.0, 1.0)      # Value = 245.0

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

    color_function = create_color_transfer_function(structure)
    opacity_function = create_opacity_transfer_function(structure)

    render_window, interactor = create_render_window(volume_mapper, color_function, opacity_function)
    render_window.Render()
    interactor.Start()

if __name__ == "__main__":
    mhd_file = "E:/Documents/OneDrive - Pontificia Universidad Javeriana/Trabajos_pontifarras/Octavo_Semestre/Tesis/Codigo/CodigoBase/Data/raw/patient.mhd"
    
    # Selecciona la estructura a visualizar:
    ## Everything = 1
    ## Everything (alt) = 2
    ## Electrodes and brain = 3
    ## Electrodes = 4
    
    structure_to_render = 4
    render_mhd_structure(mhd_file, structure_to_render)


