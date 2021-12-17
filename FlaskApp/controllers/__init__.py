from controllers.project_controller import projects
from controllers.user_controller import users
from controllers.image_controller import project_images, pattern_images
from controllers.pattern_controller import patterns

# add future controllers into list
registerable_controllers = [projects, users, project_images, patterns, pattern_images]