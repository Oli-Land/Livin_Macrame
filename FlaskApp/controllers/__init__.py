from controllers.project_controller import projects
from controllers.user_controller import users
from controllers.pattern_controller import patterns
from controllers.knot_controller import knots
from controllers.cord_controller import cords
from controllers.image_controller import project_images, pattern_images, knot_images, cord_images

registerable_controllers = [projects, users, project_images, patterns, pattern_images, knots, knot_images, cords, cord_images]