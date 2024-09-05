import vedo

print("vedo", vedo.__version__)
sphere = vedo.Sphere().linewidth(1)
plt = vedo.Plotter()
plt += sphere
plt.show(axes=1, viewup='z', zoom=1.5)