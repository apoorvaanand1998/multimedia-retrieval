
- download data and read find https://www.opengl.org/ python integration
- https://pyopengl.sourceforge.net/


### Step 1
#### Step introduction:
- description/goal of the step
- 
#### notations:
- Vertex notation, edge notation, face 'notation', mesh, mesh cells, cell vertices, data attributes 

### explanations 
- wireframe simple outline
- meshing variability
- screenshots of frontend

We tried several libraries for viewing the shapes:
- Vedo: https://vedo.embl.es/ 
- Open3d: https://www.open3d.org/
- Pymesh

## Step 2
#### Step introduction:
- description/goal of the step
- 
#### Step 2.1: Analyzing a single shape
We created a simple pipeline/tool with {library} where for each shape
- output class
- the number of faces and vertices of the shape
- the type of faces (e.g. only triangles, only quads, mixes of triangles and quads)
- the axis-aligned 3D bounding box of the shapes
#### Step 2.2: Statistics over the whole database
A post-processing function gathers several shape metrics (number of vertices, number of faces, shape class) to create a histogram. Consequently, these numbers are used to generate an average shape and a x percentile range of outliers
#### Step 2.3. Resampling outliers
