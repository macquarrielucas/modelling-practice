from fenics import *
from mshr import *
import matplotlib.pyplot as plt
import numpy as np
domain = Circle(Point(0,0),1)
mesh = generate_mesh(domain,64)
V=FunctionSpace(mesh,'P',1)

#Define boundary conditions
def boundary(x,on_boundary):
    return on_boundary
w_D=Constant(0)
bc = DirichletBC(V,w_D,boundary)


#Define variational problem
beta=8
R0=0.6
p = Expression('4*exp(-pow(beta,2)*(pow(x[0],2)+pow(x[1]-R0,2)))',degree=1,beta=beta,R0=R0)
w = TrialFunction(V)
v = TestFunction(V)
a=dot(grad(w),grad(v))*dx
L=p*v*dx

#Compute Solution
w=Function(V)
solve(a==L,w, bc)
#Plot solution and mesh
#plot(w, title='Deflection')
#load the expression into a function
p=interpolate(p,V)
#plot(p, title='Load')

#collect the data
vtkfile_w = File('poisson_membrane/deflection.pvd')
vtkfile_w << w
vtkfile_p = File('poisson_membrane/load.pvd')
vtkfile_p << p
#plot(mesh)
#plt.show()

#Curve plot along x=0 comparing p and w
tol = 0.001
y=np.linspace(-1+tol, 1- tol, 101) #avoid hitting points outside the domain
points=[(0,y_) for y_ in y] #2D points
w_line = np.array([w(point) for point in points])
p_line = np.array([p(point) for point in points])
plt.plot(y, 50*w_line, 'k', linewidth=2)
plt.plot(y, p_line, 'b--', linewidth=2)
plt.grid(True)
plt.xlabel('$y$')
plt.legend(['Deflection ($\\times 50$)', 'Load'], 'loc=upper left')

plt.show()

