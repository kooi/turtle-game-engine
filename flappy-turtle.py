import random
import time
import turtle

# setup
# tine = player
tina = turtle.Turtle()
tina.shape("turtle")
tina.color("dark green")
tina.penup()

# larry does object-drawing (and blanking)
larry = turtle.Turtle()
larry.shape("turtle")
larry.color("green")
larry.penup()
larry.hideturtle()


screen_max_y = 180
screen_min_y = -180
screen_max_x = 180
screen_min_x = -180
pipe_opening_height = 50
pipe_width = 50
flap_dvy = 18
pipes_array_size = 2

ax = 0
ay = -1.2

vx = 4
vy = 0

sx = 0
sy = 100

tina.goto(sx, sy)

turtle.Screen().tracer(0)


# input handler
def flap(x, y):
    global vy
    vy += flap_dvy


def create_pipes(n, ps):
    # ps = []
    dx_min = 150
    dx_max = 300
    y_min = -150
    y_max = +150

    for i in range(n):
        px = 0
        if i + len(ps) > 0:
            px = ps[i - 1]["x"]

        ps.append(
            {
                "x": px + random.randrange(dx_min, dx_max),
                "y": random.randrange(y_min, y_max),
            }
        )
    return ps


# pipes = [{"x": 100, "y": 75}, {"x": 300, "y": 25}]
pipes = create_pipes(pipes_array_size, [])


def draw_pipe(t, p):
    t.color("green")
    t.penup()
    t.goto(p["x"], p["y"])

    t.left(90)
    t.forward(pipe_opening_height / 2)

    h = screen_max_y - t.pos()[1]
    w = pipe_width

    t.pendown()
    t.begin_fill()
    for i in range(2):
        t.forward(h)
        t.right(90)
        t.forward(w)
        t.right(90)
    t.right(90)
    t.end_fill()
    t.penup()

    t.right(90)
    t.forward(pipe_opening_height)

    h = t.pos()[1] - screen_min_y
    w = pipe_width

    t.pendown()
    t.begin_fill()
    for i in range(2):
        t.forward(h)
        t.left(90)
        t.forward(w)
        t.left(90)
    t.right(270)
    t.end_fill()
    t.penup()


def draw_blank(t, c):
    t.home()
    t.color(c)
    t.dot(screen_max_x * 4)


def is_inside(pos, pipe):
    # within pipe x_bounds
    if pos[0] > pipe["x"] and pos[0] < pipe["x"] + pipe_width:
        # above hole
        if pos[1] > pipe["y"] + pipe_opening_height / 2:
            return True
        # below hole
        if pos[1] < pipe["y"] - pipe_opening_height / 2:
            return True
    return False


turtle.Screen().onclick(flap)
dead = False

# gameloop
# while True:
# for t in range(200):  # 10s
while not dead:
    # turtle.clear()
    # turtle.Screen().bgcolor("light blue")
    draw_blank(larry, "light blue")
    # update physics
    x = tina.pos()[0]
    y = tina.pos()[1]

    vx = vx + ax
    vy = vy + ay

    # ltr-movement centres on tina
    # x = x + vx
    y = y + vy

    # ltr-movement is rtl-movement of pipes
    for p in pipes:
        p["x"] = p["x"] - vx

    # do collisions
    # screen_edge
    if y > screen_max_y:
        y = screen_max_y
        vy = 0
    if y < screen_min_y:
        y = screen_min_y
        vy = 0

    if x > screen_max_x:
        x = screen_min_x
    # pipes
    for pipe in pipes:
        if is_inside([x, y], pipe):
            dead = True

    # update drawing
    #    draw background
    #    draw pipes
    for p in pipes:
        if p["x"] < 200 and p["x"] > -200:
            draw_pipe(larry, p)
        if p["x"] < -200:
            pipes.remove(p)
            pipes = create_pipes(1, pipes)
    #    draw tina
    tina.goto(x, y)
    time.sleep(0.03)
    turtle.Screen().update()

tina.color("red")
tina.write("   Oh, woe is me!", font=("Times New Roman", 16, "italic"))
turtle.Screen().update()
