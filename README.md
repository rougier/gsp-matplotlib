# Introduction

The Graphic Server Protocol (GSP) is meant to be an API between hardware and software, targeted at developpers who do not want to dive into the arcane of [OpenGL], [Metal] or [Vulkan] but still want to benefit from GPU speed, versatily and quality.

The overall goal of GSP is not to provide a general graphics API but rather to address **only** scientific visualization, which requires a far fewer number of objects and concepts, with specific requirements on rendering quality though. The API is voluntarily small and targets the smallest set of visuals that allow to render the vast majority of scientific plots (2d or 3d).

[OpenGL]: https://www.opengl.org
[Metal]: https://developer.apple.com/metal
[Vulkan]: https://www.vulkan.org/


# Status

## Core

- [x] [core.Data]() - encapsulate raw data (any type)
- [x] [core.Buffer]() - a structured view on raw data
- [x] [core.Canvas]() - create a drawing surface  
- [x] [core.Viewport]() - define a region over a drawing surface
- [ ] core.Texture - define a 1D, 2D or 3D Buffer
- [x] [core.Measure]() - define a value with unit
- [x] [core.Color]() - define a color
- [x] [core.Marker]() - define a marker type

## Visual

**Zero dimension**

* [x] [visual.Pixels]() - create a collection of pixels
* [x] [visual.Points]() - create a collection of points
* [x] [visual.Markers]() - create a collection of markers

**One dimension**

* [ ] visual.Segments - create a collection of line segments
* [ ] visual.Lines - create a collection of straight lines
* [ ] visual.Paths - create a collection of smooth lines

**Two dimensions**

* [ ] visual.Triangles - create a collection of triangles
* [ ] visual.Polygons - create a collection of polygons
* [ ] visual.Glyphs - create a collection of glyphs

**Three dimensions**

* [x] [visual.Mesh]() - create a mesh
* [ ] visual.Volume - create a volume

## Transform

**Base**

* [x] [transform.Transform]() - Generic transform

**Colors**

* [x] [transform.Colormap]() - map a scalar to a color  (`T[1] → T[4]`)
* [x] [transform.Light]() - modify a color according to a light  (`T[n,3] → T[n,4]`)

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

  * [x] [transform.Screen]() - Screen coordinates
  * [x] [transform.ScreenX]() - Screen X coordinates
  * [x] [transform.ScreenY]() - Screen X coordinates
  * [x] [transform.ScreenZ]() - Screen X coordinates

**Measure**  (`T[n] → T[n]`)

  * [x] [transform.Pixel]() - Conversion to pixel
  * [x] [transform.Point]() - Conversion to point (1/72 inch)
  * [x] [transform.Inch]() - Conversion to inch
  * [x] [transform.Millimeter]() - Conversion to millimeter
  * [x] [transform.Centimeter]() - Conversion to centimeter
  * [x] [transform.Meter]() - Conversion to meter
  * [x] [transform.Kilometer]() - Conversion to kilometer
