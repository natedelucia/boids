import random
import tkinter as tk
import math

from numpy import delete

# Defaults and Constants
BG = "#000000"
FG = "#043bad"
CANVASHEIGHT = 768
CANVASWIDTH = 1024
DELAY = 100

BOIDHEIGHT = 20
BOIDWIDTH = 10
MINSPEED = 2
MAXSPEED = 5
TURNSPEED = 2
INNERRANGE = 50
OUTERRANGE = 100
AVOIDANCE = 0.1  # 0-1
SHOWINNER = True
SHOWOUTER = False

NUMBOIDS = 50
INITIALDENSITY = 0.75  # 0-1


class Boid:
    def __init__(self, x, y, vx, vy, height=BOIDHEIGHT, width=BOIDWIDTH, color=FG):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.height = height
        self.width = width
        self.color = color
        self.wingAngle = math.atan(width / height) * 180 / math.pi
        self.wingDistance = (width / 2) / math.sin(self.wingAngle * math.pi / 180)

    def draw(self, canvas: tk.Canvas, gen: int) -> None:
        if self.vx == 0:
            direction = -90 if self.vy < 0 else 90
        else:
            direction = math.atan(self.vy / self.vx) * 180 / math.pi if self.vx > 0 else 180 - -1 * math.atan(self.vy / self.vx) * 180 / math.pi

        headx = (math.cos(direction * math.pi / 180) * (BOIDHEIGHT / 2)) + self.x
        heady = (math.sin(direction * math.pi / 180) * (BOIDHEIGHT / 2)) + self.y

        leftx = (
            math.cos((direction + 180 - self.wingAngle) * math.pi / 180)
            * (self.wingDistance)
        ) + self.x
        lefty = (
            math.sin((direction + 180 - self.wingAngle) * math.pi / 180)
            * (self.wingDistance)
        ) + self.y

        tailx = (
            math.cos((direction + 180.0) * math.pi / 180) * (BOIDHEIGHT / 4)
        ) + self.x
        taily = (
            math.sin((direction + 180.0) * math.pi / 180) * (BOIDHEIGHT / 4)
        ) + self.y

        rightx = (
            math.cos((direction + 180 + self.wingAngle) * math.pi / 180)
            * (self.wingDistance)
        ) + self.x
        righty = (
            math.sin((direction + 180 + self.wingAngle) * math.pi / 180)
            * (self.wingDistance)
        ) + self.y

        canvas.create_polygon(
            headx,
            heady,
            leftx,
            lefty,
            tailx,
            taily,
            rightx,
            righty,
            fill=self.color,
            tags="gen" + str(gen),
        )
        if SHOWINNER:
            canvas.create_oval(
                self.x - INNERRANGE / 2,
                self.y - INNERRANGE / 2,
                self.x + INNERRANGE / 2,
                self.y + INNERRANGE / 2,
                outline="red",
                tags="gen" + str(gen),
            )
        if SHOWOUTER:
            canvas.create_oval(
                self.x - OUTERRANGE / 2,
                self.y - OUTERRANGE / 2,
                self.x + OUTERRANGE / 2,
                self.y + OUTERRANGE / 2,
                outline="green",
                tags="gen" + str(gen),
            )

    def update(self, boids: list["Boid"]) -> None:
        inner_dx = inner_dy = 0
        for boid in boids:
            dist = self.distTo(boid)
            if dist < INNERRANGE and dist != 0:
                inner_dx += self.x - boid.x
                inner_dy += self.y - boid.y
        self.vx += inner_dx * AVOIDANCE
        self.vy += inner_dy * AVOIDANCE
        
        self.vx = min(self.vx, MAXSPEED) if self.vx > 0 else max(self.vx, -1 * MAXSPEED)
        self.vy = min(self.vy, MAXSPEED) if self.vy > 0 else max(self.vy, -1 * MAXSPEED)

        self.x += self.vx
        self.y += self.vy

    def distTo(self, other: "Boid") -> float:
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)


def createBoids() -> list[Boid]:
    boids = []
    cx = CANVASWIDTH / 2
    cy = CANVASHEIGHT / 2
    for _ in range(NUMBOIDS):
        x = random.randint(
            int(cx - (CANVASWIDTH * 0.5 * (1 - INITIALDENSITY))),
            int(cx + (CANVASWIDTH * 0.5 * (1 - INITIALDENSITY))),
        )
        y = random.randint(
            int(cy - (CANVASHEIGHT * 0.5 * (1 - INITIALDENSITY))),
            int(cy + (CANVASHEIGHT * 0.5 * (1 - INITIALDENSITY))),
        )
        vx = random.randint(MINSPEED, MAXSPEED) * random.choice((-1, 1))
        vy = random.randint(MINSPEED, MAXSPEED) * random.choice((-1, 1))
        boids.append(Boid(x, y, vx, vy))
    return boids


def main():
    root = tk.Tk()
    root.resizable(False, False)
    canvas = tk.Canvas(root, bg=BG, height=CANVASHEIGHT, width=CANVASWIDTH, bd=0)
    canvas.pack()
    boids = createBoids()
    gen = 0
    while True:
        for boid in boids:
            boid.update(boids)
            # boid.direction += random.randint(0, 2)
            # boid.x += int(math.cos(-1 * boid.direction * math.pi / 180) * 3)
            # boid.y += int(math.sin(-1 * boid.direction * math.pi / 180) * 3)
            boid.draw(canvas, gen)
        for _ in range(len(boids) * 2):
            canvas.delete("gen" + str(gen - 1))
        gen += 1
        root.after(DELAY, func=None)
        root.update()
    canvas.mainloop()


if __name__ == "__main__":
    main()
