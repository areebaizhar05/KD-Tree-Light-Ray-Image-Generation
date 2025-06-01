import math
from PIL import Image


# 3-tuple based vector utilities
def vector(x, y, z):
    """Creates a 3-component vector as a tuple of floats."""
    return (float(x), float(y), float(z))


def vector_addition(v1, v2):
    """Returns the addition of two vectors."""
    return (v1[0] + v2[0], v1[1] + v2[1], v1[2] + v2[2])


def vector_subtraction(v1, v2):
    """Returns the subtraction of two vectors."""
    return (v1[0] - v2[0], v1[1] - v2[1], v1[2] - v2[2])


def dot_product(v1, v2):
    """Returns the dot product of two vectors."""
    return (v1[0] * v2[0]) + (v1[1] * v2[1]) + (v1[2] * v2[2])


def length_of_vector(v):
    """Returns the magnitude of a vector."""
    return math.sqrt(dot_product(v, v))


def normalize(v):
    """Returns the unit vector in the direction of v."""
    norm = length_of_vector(v)
    if norm == 0:
        return (0.0, 0.0, 0.0)
    return (v[0] / norm, v[1] / norm, v[2] / norm)


class Ray:
    """Ray with origin and direction (unit vector)."""

    def __init__(self, origin, direction):
        self.origin = origin  # tuple of floats
        self.direction = normalize(direction)


def create_sphere(center, radius):
    """returns a tuple with center coordinates and radius."""
    return (center, radius)


def center(sphere):
    return sphere[0]


def radius(sphere):
    return sphere[1]


def intersect(sphere, ray):
    """Ray-sphere intersection. Returns smallest positive t or None."""
    oc = vector_subtraction(ray.origin, center(sphere))
    a = dot_product(ray.direction, ray.direction)
    b = 2.0 * dot_product(oc, ray.direction)
    c = dot_product(oc, oc) - radius(sphere) * radius(sphere)
    discriminant = b * b - 4 * a * c

    if discriminant < 0:
        return None, None

    sqrt_d = math.sqrt(discriminant)
    t1 = (-b - sqrt_d) / (2 * a)
    t2 = (-b + sqrt_d) / (2 * a)

    if t1 > 0 and t2 > 0:
        return min(t1, t2), sphere
    elif t1 > 0:
        return t1, sphere
    elif t2 > 0:
        return t2, sphere
    return None, None


# KD-tree as nested dictionaries
def build_kd_tree(objects, depth=0):
    """Builds a KD-tree represented as nested dicts."""
    if not objects:
        return {} #changed to dict from none
    axis = depth % 3

    def sort_key(obj):
        if axis == 0:
            return center(obj)[0]
        elif axis == 1:
            return center(obj)[1]
        else:
            return center(obj)[2]

    objects.sort(key=sort_key)
    median = len(objects) // 2
    # Create dict node
    return {
        "value": objects[median],  # store the Sphere object
        "left": build_kd_tree(objects[:median], depth + 1),
        "right": build_kd_tree(objects[median + 1 :], depth + 1),
    }


def intersect_kd_tree(ray, node):
    if node=={}:
        return None, None
    best_t, best_sphere = None, None
    # Test current node sphere
    result = intersect(node["value"], ray) ##
    if result is not None:
        best_t, best_sphere = result
    # Recurse left
    lt, ls = intersect_kd_tree(ray, node["left"]) ##
    if lt is not None and (best_t is None or lt < best_t):
        best_t, best_sphere = lt, ls
    # Recurse right
    rt, rs = intersect_kd_tree(ray, node["right"])
    if rt is not None and (best_t is None or rt < best_t):
        best_t, best_sphere = rt, rs
    return best_t, best_sphere


def shade(hit_point, sphere, light):
    normal = normalize(vector_subtraction(hit_point, center(sphere)))
    light_dir = normalize(vector_addition(light, hit_point))
    diffuse = max(0, dot_product(normal, light_dir))
    return int(255 * diffuse)


def desired_image(distance, angle, radius):
    return distance, angle, radius


def render(width, height, sphere, dist="", dir="", angle=""):
    image = Image.new("RGB", (width, height))
    pixels = image.load()

    # Create an empty image
    # Define camera and scene
    if dist.lower() == "s":
        dist = -1.0
    elif dist.lower() == "m":
        dist = -10.0
    elif dist.lower() == "l":
        dist = -20.0
    else:
        return "Invalid option"

    # direction in plane of screen
    if dir.lower() == "tl":
        dir = (-2, -2)
    elif dir.lower() == "br":
        dir = (2, 2)
    elif dir.lower() == "tr":
        dir = (2, -2)
    elif dir.lower() == "bl":
        dir = (-2, 2)
    elif dir.lower() == "l":
        dir = (-2, 0)
    elif dir.lower() == "r":
        dir = (2, 0)
    elif dir.lower() == "b":
        dir = (0, 2)
    elif dir.lower() == "t":
        dir=(0, -2)
    else:
        return "Invalid option"
    # angle perpendicular to plane of screen
    if angle.lower() == "l":
        angle = (-1,)
    elif angle.lower() == "m":
        angle = (-3,)
    elif angle.lower() == "h":
        angle = (-10,)
    else:
        return "Invalid option"

    camera = (0.0, 0, dist)
    # sphere = create_sphere((-0.15, -0.3, 4), 1)
    # light = (0, -2, -10)
    # print(type(dir),type(angle))
    light = dir + angle

    for y in range(height):
        for x in range(width):
            u = (x / width) * 2 - 1
            v = (y / height) * 2 - 1
            v *= height / width

            ray = Ray(camera, (vector_subtraction((u, v, 0), camera)))

            hit = intersect(sphere, ray)
            if hit[0] is not None:
                # unpack
                t, hit_sphere = hit

                # compute hit-point
                offset = (
                    ray.direction[0] * t,
                    ray.direction[1] * t,
                    ray.direction[2] * t,
                )
                hit_point = vector_addition(ray.origin, offset)

                # shade with correct light_dir
                color = shade(hit_point, hit_sphere, light)
                pixels[x, y] = (color, color, color)
            else:
                pixels[x, y] = (0, 0, 0)

    # Save the image
    image.save("output.png")


def main():
    sphere1 = create_sphere((-0.15, -0.3, 4), 1.0)
    sphere2 = create_sphere((3.0, 4.0, 0.0), 1.0)
    sphere3 = create_sphere((0.5, 1.0, 2.7), 1.0)
    sphere4 = create_sphere((0.7, 4.0, 4.0), 1.0)
    spheres = [sphere1, sphere2, sphere3, sphere4]
    ray = Ray((0, 0, 0), (-0.15, -0.3, 4.0))
    kd_tree = build_kd_tree(spheres)
    # print(kd_tree)
    t, sphere = intersect_kd_tree(ray, kd_tree)
    # print(t, sphere)
    assert t is not None, "No intersection found"
    print(f"Intersection at t = {t}")

    dist = input("Enter size of the sphere: small(S), medium(M), large(L)")
    dir = input(
        "Modify direction in plane of screen: topright(tr),topleft(tl), bottomright(br), bottomleft(bl), left(l), right(r), bottom(b), top(t)"
    )
    angle = input("Angle: low(l), medium(m), high(h)")
    render(400, 400, sphere, dist, dir, angle)


if __name__ == "__main__":
    main()
