# HPX Project

Repository containing the HPX implementation of the nonlinear system Identification 
with Gaussian processes minimal working example used for "Scalability of Gaussian 
Processes with Asynchronous Tasks: A Comparison between HPX and PETSc", 
extended with uncertainty and optimization.

## Docker Containers

### Release (HPX installed in Release mode)

Build image inside hpx_project folder:  
`sudo docker build . -f docker/Dockerfile_release -t hpx_release_image`  
Start container:  
`sudo docker run -it --rm --user user hpx_release_image`  

### Debug (HPX installed in Debug mode)

Build image inside hpx_project folder:  
`sudo docker build . -f docker/Dockerfile_debug -t hpx_debug_image`  
Start container:  
`sudo docker run -it --rm --user user hpx_debug_image`  

## Compile and Run Benchmark

Benchmark Script:  
`cd && cd hpx_project && ./run_benchmarks.sh cpu/gpu/blas`  
