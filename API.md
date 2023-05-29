
# Graphic Server Protocol

The Graphic Server Protocol (GSP) is meant to be an API between hardware and software, targeted at developpers who do not want to dive into the arcane of [OpenGL](https://www.opengl.org/), [Metal](https://developer.apple.com/metal/) or [Vulkan](https://www.vulkan.org/). The overall goal of GSP is not to provide a general graphics API but rather to address scientific visualization, which requires a far fewer number of objects and concepts, with specific requirements on rendering quality though.

* [Core](#core)
* [Transform](#transform)  
* [Visual](#visual)

## Matplotlib implementation

### [Core]()

* [x] [core.Canvas]() - create a drawing surface  
* [x] [core.Viewport]() - define a region over a drawing surface
* [ ] [core.Data]() - encapsulate raw data (any type)
* [x] [core.Buffer]() - a structured view on raw data
* [ ] [core.Texture]() - define a 1D, 2D or 3D Buffer
* [x] [core.Color]() - define a color

### [Visual]()

#### Zero dimension

* [x] [visual.Pixels]() - create a collection of pixels
* [x] [visual.Points]() - create a collection of points
* [ ] [visual.Markers]() - create a collection of markers

#### One dimension

* [ ] [visual.Segments]() - create a collection of line segments
* [ ] [visual.Lines]() - create a collection of straight lines
* [ ] [visual.Paths]() - create a collection of smooth lines

#### Two dimensions

* [ ] [visual.Triangles]() - create a collection of triangles
* [ ] [visual.Polygons]() - create a collection of polygons
* [ ] [visual.Glyphs]() - create a collection of glyphs

#### Three dimensions

* [x] [visual.Mesh]() - create a mesh
* [ ] [visual.Volume]() - create a volume


### [Transform]()

#### Base

* [x] [transform.Transform]() - Generic transform

#### Arithmetic operators
  
* [x] [transform.Add]() - Addition
* [x] [transform.Sub]() - Subtraction
* [x] [transform.Mul]() - Multiplication
* [x] [transform.Div]() - Division

#### Geometry / Color accessors

* [x] [transform.X]() / [transform.R]() - First component
* [x] [transform.Y]() / [transform.G]() - Second component
* [x] [transform.Z]() / [transform.B]() - Third component
* [x] [transform.W]() / [transform.A]() - Fourth component

#### Datetime accessors

* [ ] [transform.Second]() - Access to second
* [ ] [transform.Minute]() - Access to minute
* [ ] [transform.Hour]() - Access to hour
* [ ] [transform.Day]() - Access to day
* [ ] [transform.Month]() - Access to month
* [ ] [transform.Year]() - Access to year

#### Geometry

* [ ] [transform.Scale]() - Abritrary scaling
* [ ] [transform.Translate]() - Arbitraty translation
* [ ] [transform.Rotate]() - Arbitraty rotation
* [ ] [transform.MVP]() - Model / View / Projection 

#### Screen access (JIT)

  * [ ] [transform.ScreenX]() - Screen X coordinates
  * [ ] [transform.ScreenY]() - Screen Y coordinates
  * [x] [transform.ScreenZ]() - Screen Z (depth) coordinates 

#### Measure conversion

  * [ ] [transform.Pixel]() - Conversion to pixel
  * [ ] [transform.Point]() - Conversion to point (1/72 inch)
  * [ ] [transform.Inch]() - Conversion to inch
  * [ ] [transform.Millimeter]() - Conversion to millimeter
  * [ ] [transform.Centimeter]() - Conversion to centimeter
  * [ ] [transform.Meter]() - Conversion to meter

#### Time conversion

  * [ ] [transform.Second]() - Conversion to seconds
  * [ ] [transform.Minute]() - Conversion to minutes
  * [ ] [transform.Hour]() - Conversion to hours
  * [ ] [transform.Day]() - Conversion to days
  * [ ] [transform.Month]() - Conversion to month
  * [ ] [transform.Year]() - Conversion to years

#### Miscellaneous

* [x] [transform.Colormap]() - map a scalar to a color
* [ ] [transform.Light]() - modify a color according to a light
* [ ] [transform.Join]() - join several transforms


  
