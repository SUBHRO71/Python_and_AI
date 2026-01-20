import tkinter as tk
import turtle

def expand_lsystem(axiom, rules, iterations):
    current = axiom
    for _ in range(iterations):
        next_string = []
        for char in current:
            next_string.append(rules.get(char, char))
        current = "".join(next_string)
    return current


def draw_lsystem(t, screen, instructions, angle, step):
    stack = []
    length = len(instructions)

    screen.tracer(0, 0)

    for i, cmd in enumerate(instructions):
        color_value = i / length
        t.pencolor(color_value, 0.6, 1 - color_value)

        if cmd == "F":
            t.forward(step)
        elif cmd == "+":
            t.right(angle)
        elif cmd == "-":
            t.left(angle)
        elif cmd == "[":
            stack.append((t.position(), t.heading()))
        elif cmd == "]":
            pos, heading = stack.pop()
            t.penup()
            t.goto(pos)
            t.setheading(heading)
            t.pendown()

    screen.update()


def generate():
    t.clear()
    t.penup()
    t.goto(0, -250)
    t.setheading(90)
    t.pendown()

    axiom = axiom_entry.get()
    angle = float(angle_entry.get())
    iterations = int(iter_entry.get())

    rules = {}
    rule_lines = rules_entry.get("1.0", tk.END).strip().split("\n")
    for line in rule_lines:
        if ":" in line:
            key, value = line.split(":")
            rules[key.strip()] = value.strip()

    final_string = expand_lsystem(axiom, rules, iterations)
    draw_lsystem(t, screen, final_string, angle, step=5)


root = tk.Tk()
root.title("L-System Fractal Architect")

left_frame = tk.Frame(root)
left_frame.pack(side=tk.LEFT, padx=10)

right_frame = tk.Frame(root)
right_frame.pack(side=tk.RIGHT)

canvas = tk.Canvas(right_frame, width=600, height=600)
canvas.pack()

screen = turtle.TurtleScreen(canvas)
screen.bgcolor("black")
screen.colormode(1.0)

t = turtle.RawTurtle(screen)
t.hideturtle()
t.speed(0)
t.pensize(1)

tk.Label(left_frame, text="Axiom").pack(anchor="w")
axiom_entry = tk.Entry(left_frame)
axiom_entry.insert(0, "F")
axiom_entry.pack(fill="x")

tk.Label(left_frame, text="Rules (one per line, e.g. F:F+F-F)").pack(anchor="w")
rules_entry = tk.Text(left_frame, height=5)
rules_entry.insert("1.0", "F:F+F-F")
rules_entry.pack(fill="x")

tk.Label(left_frame, text="Angle").pack(anchor="w")
angle_entry = tk.Entry(left_frame)
angle_entry.insert(0, "90")
angle_entry.pack(fill="x")

tk.Label(left_frame, text="Iterations").pack(anchor="w")
iter_entry = tk.Entry(left_frame)
iter_entry.insert(0, "4")
iter_entry.pack(fill="x")

tk.Button(left_frame, text="Generate", command=generate).pack(pady=10)

root.mainloop()
