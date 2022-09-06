# Seaborn Grasshopper
A Rhino Remote library that brings Seaborn (Matplotlib) inside of Grasshopper using [Hops](https://github.com/mcneel/compute.rhino3d/tree/master/src/ghhops-server-py). 

This second version is a complete refactor of the seaborn-grasshopper implementation. This approach greatly improves from the first version in the following ways:
- Additional fuctions added
    - `despine`     Dictionary with "Despine" functions arguments, that removes top and right axis lines. 
    - `add_args`    Use additional figure arguments are not implemented in Grasshopper. 
    - `ax_args`     Implement axis arguments to the matplotlib.Axis element. (Set title, x and y limits, etc ) 
    - `fig_size`    Change figure size
- Ready for web deployment using Heroku and gunicorn
- Export image as a encoded b64 string
- Less code duplication
- Correct handling of defaults
- Style improvement


## More information
More infromation on how to use the tool [comming soon](). 

## Typical workflow
![Seaborn Grasshopper](https://i.imgur.com/MUZLQhk.gif)
Author : Pablo Arango

## Result examples
![image](https://user-images.githubusercontent.com/39027094/181036912-2712bd6c-5ec7-4969-8260-b261391a7485.png)
Author : MaesAntoine

# Deployment
Follow [this tutorial](https://www.youtube.com/watch?v=SiCAIRc0pEI). The code is already set-up to work with Heroku.



