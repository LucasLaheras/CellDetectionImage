# !/usr/bin/env python
import itk
import cv2
import numpy as np


def levelsetITK(inputFileName, outputFileName, seedPosX, seedPosY, initialDistance, sigma, alpha, beta,
                propagationScaling, numberOfIterations):

    seedValue = -initialDistance

    Dimension = 2

    InputPixelType = itk.F
    OutputPixelType = itk.UC

    InputImageType = itk.Image[InputPixelType, Dimension]
    OutputImageType = itk.Image[OutputPixelType, Dimension]

    ReaderType = itk.ImageFileReader[InputImageType]
    WriterType = itk.ImageFileWriter[OutputImageType]

    reader = ReaderType.New()
    reader.SetFileName(inputFileName)

    # First we include the header of the CurvatureAnisotropicDiffusionImageFilter that will be used for removing noise
    # from the input image
    SmoothingFilterType = itk.CurvatureAnisotropicDiffusionImageFilter[
        InputImageType, InputImageType]
    smoothing = SmoothingFilterType.New()
    smoothing.SetTimeStep(0.125)
    smoothing.SetNumberOfIterations(5)
    smoothing.SetConductanceParameter(9.0)
    smoothing.SetInput(reader.GetOutput())

    # Together, these two filters will produce the image potential for regulating the speed term in the differential
    # equation describing the evolution of the level set.
    GradientFilterType = itk.GradientMagnitudeRecursiveGaussianImageFilter[
        InputImageType, InputImageType]
    gradientMagnitude = GradientFilterType.New()
    gradientMagnitude.SetSigma(sigma)
    gradientMagnitude.SetInput(smoothing.GetOutput())

    SigmoidFilterType = itk.SigmoidImageFilter[InputImageType, InputImageType]
    sigmoid = SigmoidFilterType.New()
    sigmoid.SetOutputMinimum(0.0)
    sigmoid.SetOutputMaximum(1.0)
    sigmoid.SetAlpha(alpha)
    sigmoid.SetBeta(beta)
    sigmoid.SetInput(gradientMagnitude.GetOutput())

    FastMarchingFilterType = itk.FastMarchingImageFilter[
        InputImageType, InputImageType]
    fastMarching = FastMarchingFilterType.New()

    # Aplicação do level set
    GeoActiveContourFilterType = itk.GeodesicActiveContourLevelSetImageFilter[
        InputImageType, InputImageType, InputPixelType]
    geodesicActiveContour = GeoActiveContourFilterType.New()
    geodesicActiveContour.SetPropagationScaling(propagationScaling)
    geodesicActiveContour.SetCurvatureScaling(1.0)
    geodesicActiveContour.SetAdvectionScaling(1.0)
    geodesicActiveContour.SetMaximumRMSError(0.02)
    geodesicActiveContour.SetNumberOfIterations(numberOfIterations)
    geodesicActiveContour.SetInput(fastMarching.GetOutput())
    geodesicActiveContour.SetFeatureImage(sigmoid.GetOutput())

    # The time-crossing map resulting from the FastMarchingImageFilter will be thresholded using the BinaryThresholdImageFilter
    ThresholdingFilterType = itk.BinaryThresholdImageFilter[
        InputImageType, OutputImageType]
    thresholder = ThresholdingFilterType.New()
    # The upper threshold passed to the BinaryThresholdImageFilter will define the time snapshot that we
    # are taking from the time-crossing map. In an ideal application the user should be able to select this
    # threshold interactively using visual feedback
    thresholder.SetLowerThreshold(-1000.0)
    thresholder.SetUpperThreshold(0.0)
    thresholder.SetOutsideValue(itk.NumericTraits[OutputPixelType].min())
    thresholder.SetInsideValue(itk.NumericTraits[OutputPixelType].max())
    thresholder.SetInput(geodesicActiveContour.GetOutput())

    seedPosition = itk.Index[Dimension]()
    seedPosition[0] = seedPosX
    seedPosition[1] = seedPosY

    node = itk.LevelSetNode[InputPixelType, Dimension]()
    node.SetValue(seedValue)
    node.SetIndex(seedPosition)

    seeds = itk.VectorContainer[
        itk.UI, itk.LevelSetNode[InputPixelType, Dimension]].New()
    seeds.Initialize()
    seeds.InsertElement(0, node)

    fastMarching.SetTrialPoints(seeds)
    fastMarching.SetSpeedConstant(1.0)

    CastFilterType = itk.RescaleIntensityImageFilter[
        InputImageType, OutputImageType]

    caster1 = CastFilterType.New()
    caster2 = CastFilterType.New()
    caster3 = CastFilterType.New()
    caster4 = CastFilterType.New()

    writer1 = WriterType.New()
    writer2 = WriterType.New()
    writer3 = WriterType.New()
    writer4 = WriterType.New()

    caster1.SetInput(smoothing.GetOutput())
    writer1.SetInput(caster1.GetOutput())
    writer1.SetFileName("GeodesicActiveContourImageFilterOutput1.png")
    caster1.SetOutputMinimum(itk.NumericTraits[OutputPixelType].min())
    caster1.SetOutputMaximum(itk.NumericTraits[OutputPixelType].max())
    writer1.Update()

    caster2.SetInput(gradientMagnitude.GetOutput())
    writer2.SetInput(caster2.GetOutput())
    writer2.SetFileName("GeodesicActiveContourImageFilterOutput2.png")
    caster2.SetOutputMinimum(itk.NumericTraits[OutputPixelType].min())
    caster2.SetOutputMaximum(itk.NumericTraits[OutputPixelType].max())
    writer2.Update()

    caster3.SetInput(sigmoid.GetOutput())
    writer3.SetInput(caster3.GetOutput())
    writer3.SetFileName("GeodesicActiveContourImageFilterOutput3.png")
    caster3.SetOutputMinimum(itk.NumericTraits[OutputPixelType].min())
    caster3.SetOutputMaximum(itk.NumericTraits[OutputPixelType].max())
    writer3.Update()

    caster4.SetInput(fastMarching.GetOutput())
    writer4.SetInput(caster4.GetOutput())
    writer4.SetFileName("GeodesicActiveContourImageFilterOutput4.png")
    caster4.SetOutputMinimum(itk.NumericTraits[OutputPixelType].min())
    caster4.SetOutputMaximum(itk.NumericTraits[OutputPixelType].max())

    fastMarching.SetOutputSize(
        reader.GetOutput().GetBufferedRegion().GetSize())

    writer = WriterType.New()
    writer.SetFileName(outputFileName)
    writer.SetInput(thresholder.GetOutput())
    writer.Update()

    print(
        "Max. no. iterations: " +
        str(geodesicActiveContour.GetNumberOfIterations()) + "\n")
    print(
        "Max. RMS error: " +
        str(geodesicActiveContour.GetMaximumRMSError()) + "\n")
    print(
        "No. elpased iterations: " +
        str(geodesicActiveContour.GetElapsedIterations()) + "\n")
    print("RMS change: " + str(geodesicActiveContour.GetRMSChange()) + "\n")

    writer4.Update()

    imglvs = cv2.imread("levelset.png")
    return imglvs


def levelset(img, cX, cY):
    cv2.imwrite("histogramaLocal.png", img)
    levelsetITK("histogramaLocal.png", "levelset.png", cX, cY, 5.0, 1.0, -0.3, 2.0, 10.0, 490)
    imglvs = cv2.imread("levelset.png")
    return imglvs


def mostra(img, name='Name'):
    cv2.namedWindow(name, cv2.WINDOW_AUTOSIZE)
    cv2.imshow(name, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return


if __name__ == '__main__':
    # teste = levelsetITK("BrainProtonDensitySlice6.png", "levelset.png", 56, 92, 5.0, 1.0, -0.3, 2.0, 10.0, 490)
    levelsetITK("histogramaLocal.png", "levelset.png", 56, 92, 5.0, 1.0, -10.3, 10, 10.0, 490)

    teste = cv2.imread("GeodesicActiveContourImageFilterOutput3.png")
    """""
    lin, col, h = teste.shape

    for y in range(lin):
        for x in range(col):
            for z in range(h):
                if teste[y, x, z] < 128:
                    teste[y, x, z] = 0
                else:
                    teste[y, x, z] = 255
    """""

    mostra(teste)
