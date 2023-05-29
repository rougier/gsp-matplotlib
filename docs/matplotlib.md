
## Implementation notes

The matplotlib implementation is only a partial implementation because of several limitations:

- **Depth buffer**: matplotlib does not have a proper [depth buffer] that allows to test individual pixels. This means points/lines/triangles need to be sorted in order to draw them from back to front. Most of the time, this does the trick but there exist some situations where it is impossible to avoid problems. For example, consider two triangles that intersect each other. In in such a case, we have to decide arbitrarily which triangle will be drawn on top of the other.

- **Texture mapping**: matplotlib can manipulate images to some extent but it is not really possible to map a texture to a triangle and this limits severely the effect we can achieve with texture. Crude approximation can be achieved using higher tessellation level but this comes at the cost of speed.

- **Trilinear interpolation**: there is no easy (nor fast) way to interpolate a color inside a triangle and this limits the kind of shading we can use. Namely, we can have flat shading (per face) but not [Gouraud] (per vertex) nor [Phong] (per pixel).


The matplotlib implementation relies a lot on numpy arrays because they're compatible with the Data/Buffer approach. However, this is only a design choice and it is possible to use other approaches. The only difficulty is to control memory usage such as not to make too many copies of buffer.

[depth buffer]: https://en.wikipedia.org/wiki/Z-buffering
[Gouraud]: https://en.wikipedia.org/wiki/Gouraud_shading
[Phong]: https://en.wikipedia.org/wiki/Phong_shading


## Status

### Core

- [x] [core.Data][gsp.core.Data] - encapsulate raw data (any type)
- [x] [core.Buffer][gsp.core.Buffer] - a structured view on raw data
- [x] [core.Canvas][gsp.core.Canvas] - create a drawing surface  
- [x] [core.Viewport][gsp.core.Viewport] - define a region over a drawing surface
- [ ] core.Texture - define a 1D, 2D or 3D Buffer
- [x] [core.Measure][gsp.core.Measure] - define a value with unit
- [x] [core.Color][gsp.core.Color] - define a color
- [x] [core.Marker][gsp.core.Marker] - define a marker type

### Visual

**Zero dimension**

* [x] [visual.Pixels][gsp.visual.Pixels] - create a collection of pixels
* [x] [visual.Points][gsp.visual.Points] - create a collection of points
* [x] [visual.Markers][gsp.visual.Markers] - create a collection of markers

**One dimension**

* [ ] visual.Segments - create a collection of line segments
* [ ] visual.Lines - create a collection of straight lines
* [ ] visual.Paths - create a collection of smooth lines

**Two dimensions**

* [ ] visual.Triangles - create a collection of triangles
* [ ] visual.Polygons - create a collection of polygons
* [ ] visual.Glyphs - create a collection of glyphs

**Three dimensions**

* [x] [visual.Mesh][gsp.visual.Mesh] - create a mesh
* [ ] visual.Volume - create a volume


### Transform

**Base**

* [x] [transform.Transform][gsp.transform.Transform] - Generic transform

**Colors**

* [x] [transform.Colormap][gsp.transform.Colormap] - map a scalar to a color  (`T[1] → T[4]`)
* [x] [transform.Light][gsp.transform.Light] - modify a color according to a light  (`T[n,3] → T[n,4]`)

**Operators** (`T[n] × T[n] → T[n]`)
   
* [x] [transform.Add]() - Addition
* [x] [transform.Sub]() - Subtraction
* [x] [transform.Mul]() - Multiplication
* [x] [transform.Div]() - Division

**Accessors** (`T[n] → T[1]`)

* [x] [transform.X]() / [transform.R]() - First component
* [x] [transform.Y]() / [transform.G]() - Second component
* [x] [transform.Z]() / [transform.B]() - Third component
* [x] [transform.W]() / [transform.A]() - Fourth component
* [ ] transform.Join - join several transforms  (`T[1] × … × T[1] → T[n]`)

**Geometry** (`T[n] → T[n]`)

* [ ] transform.Scale - Arbitrary scaling
* [ ] transform.Translate - Arbitraty translation
* [ ] transform.Rotate - Arbitraty rotation
* [ ] transform.MVP - Model / View / Projection (`T[n] → T[3]`)

**Screen (JIT)** (` ∅ → T[1]`)

  * [x] [transform.Screen][gsp.transform.Screen] - Screen coordinates
  * [x] [transform.ScreenX][gsp.transform.ScreenX] - Screen X coordinates
  * [x] [transform.ScreenY][gsp.transform.ScreenY] - Screen X coordinates
  * [x] [transform.ScreenZ][gsp.transform.ScreenZ] - Screen X coordinates

**Measure**  (`T[n] → T[n]`)

  * [x] [transform.Pixel][gsp.transform.Pixel] - Conversion to pixel
  * [x] [transform.Point][gsp.transform.Point] - Conversion to point (1/72 inch)
  * [x] [transform.Inch][gsp.transform.Inch] - Conversion to inch
  * [x] [transform.Millimeter][gsp.transform.Millimeter] - Conversion to millimeter
  * [x] [transform.Centimeter][gsp.transform.Centimeter] - Conversion to centimeter
  * [x] [transform.Meter][gsp.transform.Meter] - Conversion to meter
  * [x] [transform.Kilometer][gsp.transform.Kilometer] - Conversion to kilometer
