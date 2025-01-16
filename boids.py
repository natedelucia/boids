import random
import tkinter as tk
import math

# Constants
BG = "#000000"
FG = "#043bad"
CANVASHEIGHT = 800
CANVASWIDTH = 1200
NUMBOIDS = 100
INITIALDENSITY = 0.25  # 0-1

# Defaults
BOIDHEIGHT = 20
BOIDWIDTH = 10
MINSPEED = 10
MAXSPEED = 15

INNERRANGE = 25
OUTERRANGE = 50
SHOWINNER = 0
SHOWOUTER = 0

AVOIDANCE = 0.2  # 0-1
ALIGNMENT = 0.3  # 0-1
CENTERING = 0.1  # 0-1

EDGEMARGIN = 50
TURNSTRENGTH = 1
SHOWEDGE = 0

DELAY = 25


class Settings:
    def __init__(self, root: tk.Tk, boids):
        sliderLength = 150

        height = tk.IntVar(value=BOIDHEIGHT)
        self.height = tk.Scale(
            root,
            from_=5,
            to=50,
            orient="horizontal",
            variable=height,
            label="Boid Height",
            length=sliderLength,
        )
        self.height.grid(row=0, column=1)

        width = tk.IntVar(value=BOIDWIDTH)
        self.width = tk.Scale(
            root,
            from_=5,
            to=50,
            orient="horizontal",
            variable=width,
            label="Boid Width",
            length=sliderLength,
        )
        self.width.grid(row=0, column=2)

        minSpeed = tk.IntVar(value=MINSPEED)
        self.minSpeed = tk.Scale(
            root,
            from_=2,
            to=25,
            orient="horizontal",
            variable=minSpeed,
            label="Min Speed",
            length=sliderLength,
        )
        self.minSpeed.grid(row=1, column=1)

        maxSpeed = tk.IntVar(value=MAXSPEED)
        self.maxSpeed = tk.Scale(
            root,
            from_=2,
            to=25,
            orient="horizontal",
            variable=maxSpeed,
            label="Max Speed",
            length=sliderLength,
        )
        self.maxSpeed.grid(row=1, column=2)

        innerRange = tk.IntVar(value=INNERRANGE)
        self.innerRange = tk.Scale(
            root,
            from_=10,
            to=250,
            orient="horizontal",
            variable=innerRange,
            label="Avoid Range",
            resolution=5,
            length=sliderLength,
        )
        self.innerRange.grid(row=2, column=1)

        outerRange = tk.IntVar(value=OUTERRANGE)
        self.outerRange = tk.Scale(
            root,
            from_=50,
            to=500,
            orient="horizontal",
            variable=outerRange,
            label="Follow Range",
            resolution=5,
            length=sliderLength,
        )
        self.outerRange.grid(row=2, column=2)

        avoidance = tk.DoubleVar(value=AVOIDANCE)
        self.avoidance = tk.Scale(
            root,
            from_=0,
            to=1,
            orient="horizontal",
            variable=avoidance,
            label="Avoidance",
            resolution=0.05,
            length=sliderLength,
        )
        self.avoidance.grid(row=3, column=1)

        alignment = tk.DoubleVar(value=ALIGNMENT)
        self.alignment = tk.Scale(
            root,
            from_=0,
            to=1,
            orient="horizontal",
            variable=alignment,
            label="Alignment",
            resolution=0.05,
            length=sliderLength,
        )
        self.alignment.grid(row=3, column=2)

        centering = tk.DoubleVar(value=CENTERING)
        self.centering = tk.Scale(
            root,
            from_=0,
            to=1,
            orient="horizontal",
            variable=centering,
            label="Centering",
            resolution=0.05,
            length=sliderLength,
        )
        self.centering.grid(row=4, column=1)

        turnStrength = tk.DoubleVar(value=TURNSTRENGTH)
        self.turnStrength = tk.Scale(
            root,
            from_=0,
            to=2,
            orient="horizontal",
            variable=turnStrength,
            label="Turn Strength",
            length=sliderLength,
            resolution=0.05,
        )
        self.turnStrength.grid(row=4, column=2)

        edgeMargin = tk.IntVar(value=EDGEMARGIN)
        self.edgeMargin = tk.Scale(
            root,
            from_=0,
            to=min(CANVASWIDTH, CANVASHEIGHT) / 2,
            orient="horizontal",
            variable=edgeMargin,
            label="Edge Margin",
            length=sliderLength,
            resolution=5,
        )
        self.edgeMargin.grid(row=5, column=1)

        delay = tk.IntVar(value=DELAY)
        self.delay = tk.Scale(
            root,
            from_=0,
            to=500,
            orient="horizontal",
            variable=delay,
            label="Update Delay",
            length=sliderLength,
            resolution=5,
        )
        self.delay.grid(row=5, column=2)

        self.showInner = tk.IntVar(value=SHOWINNER)
        showInner = tk.Checkbutton(
            root,
            text="Show avoidance range",
            variable=self.showInner,
            onvalue=1,
            offvalue=0,
        )
        showInner.grid(row=6, column=1, columnspan=2)

        self.showOuter = tk.IntVar(value=SHOWOUTER)
        showOuter = tk.Checkbutton(
            root,
            text="Show alignment range",
            variable=self.showOuter,
            onvalue=1,
            offvalue=0,
        )
        showOuter.grid(row=7, column=1, columnspan=2)

        self.showEdge = tk.IntVar(value=SHOWEDGE)
        showEdge = tk.Checkbutton(
            root, text="Show edge", variable=self.showEdge, onvalue=1, offvalue=0
        )
        showEdge.grid(row=8, column=1, columnspan=2)

        resetSettingsButton = tk.Button(
            root, text="Reset settings", command=lambda: resetSettings(self)
        )
        resetSettingsButton.grid(row=9, column=1, columnspan=2)

        resetSimButton = tk.Button(
            root, text="Reset simulation", command=lambda: resetBoids(boids, self)
        )
        resetSimButton.grid(row=10, column=1, columnspan=2)

        numBoids = tk.IntVar(value=NUMBOIDS)
        self.numBoids = tk.Scale(
            root,
            from_=10,
            to=500,
            orient="horizontal",
            variable=numBoids,
            label="Number of boids",
            length=sliderLength,
            resolution=10,
        )
        self.numBoids.grid(row=11, column=1)

        density = tk.DoubleVar(value=INITIALDENSITY)
        self.density = tk.Scale(
            root,
            from_=0,
            to=1,
            orient="horizontal",
            variable=density,
            label="Initial Density",
            length=sliderLength,
            resolution=0.05,
        )
        self.density.grid(row=11, column=2)


class Boid:
    def __init__(self, x, y, vx, vy, height=BOIDHEIGHT, width=BOIDWIDTH, color=FG):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.height = height
        self.width = width
        self.color = color

    def draw(self, canvas: tk.Canvas, gen: int, settings: Settings) -> None:
        if self.vx == 0:
            direction = -90 if self.vy < 0 else 90
        else:
            direction = (
                math.atan(self.vy / self.vx) * 180 / math.pi
                if self.vx > 0
                else 180 - -1 * math.atan(self.vy / self.vx) * 180 / math.pi
            )

        wingAngle = (
            math.atan(settings.width.get() / settings.height.get()) * 180 / math.pi
        )
        wingDistance = (settings.width.get() / 2) / math.sin(wingAngle * math.pi / 180)

        headx = (
            math.cos(direction * math.pi / 180) * (settings.height.get() / 2)
        ) + self.x
        heady = (
            math.sin(direction * math.pi / 180) * (settings.width.get() / 2)
        ) + self.y

        leftx = (
            math.cos((direction + 180 - wingAngle) * math.pi / 180) * (wingDistance)
        ) + self.x
        lefty = (
            math.sin((direction + 180 - wingAngle) * math.pi / 180) * (wingDistance)
        ) + self.y

        tailx = (
            math.cos((direction + 180.0) * math.pi / 180) * (settings.height.get() / 4)
        ) + self.x
        taily = (
            math.sin((direction + 180.0) * math.pi / 180) * (settings.height.get() / 4)
        ) + self.y

        rightx = (
            math.cos((direction + 180 + wingAngle) * math.pi / 180) * (wingDistance)
        ) + self.x
        righty = (
            math.sin((direction + 180 + wingAngle) * math.pi / 180) * (wingDistance)
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
        if settings.showEdge.get() == 1:
            canvas.create_polygon(
                settings.edgeMargin.get(),
                settings.edgeMargin.get(),
                CANVASWIDTH - settings.edgeMargin.get(),
                settings.edgeMargin.get(),
                CANVASWIDTH - settings.edgeMargin.get(),
                CANVASHEIGHT - settings.edgeMargin.get(),
                settings.edgeMargin.get(),
                CANVASHEIGHT - settings.edgeMargin.get(),
                outline="gray",
                fill="",
                tags="gen" + str(gen),
            )
        if settings.showInner.get() == 1:
            canvas.create_oval(
                self.x - settings.innerRange.get(),
                self.y - settings.innerRange.get(),
                self.x + settings.innerRange.get(),
                self.y + settings.innerRange.get(),
                outline="red",
                tags="gen" + str(gen),
            )
        if settings.showOuter.get() == 1:
            canvas.create_oval(
                self.x - settings.outerRange.get(),
                self.y - settings.outerRange.get(),
                self.x + settings.outerRange.get(),
                self.y + settings.outerRange.get(),
                outline="green",
                tags="gen" + str(gen),
            )

    def update(self, boids: list["Boid"], settings: Settings) -> None:
        inner_dx = inner_dy = 0
        avg_vx = avg_vy = visible_boids = 0
        avg_x = avg_y = 0
        for boid in boids:
            dist = self.distTo(boid)
            if dist < settings.innerRange.get() and dist != 0:
                inner_dx += self.x - boid.x
                inner_dy += self.y - boid.y
            if dist < settings.outerRange.get() and dist != 0:
                avg_vx += boid.vx
                avg_vy += boid.vy
                avg_x += boid.x
                avg_y += boid.y
                visible_boids += 1
        if visible_boids > 0:
            avg_vx /= visible_boids
            avg_vy /= visible_boids
            avg_x /= visible_boids
            avg_y /= visible_boids

        dvx = (
            inner_dx * settings.avoidance.get()
            + (avg_vx - self.vx) * settings.alignment.get()
            if visible_boids > 0
            else (
                0 + (avg_x - self.x) * settings.centering.get()
                if visible_boids > 0
                else 0
            )
        )
        dvy = (
            inner_dy * settings.avoidance.get()
            + (avg_vy - self.vy) * settings.alignment.get()
            if visible_boids > 0
            else (
                0 + (avg_y - self.y) * settings.centering.get()
                if visible_boids > 0
                else 0
            )
        )

        self.vx += dvx
        self.vy += dvy

        if self.x < settings.edgeMargin.get():
            self.vx += (
                settings.turnStrength.get()
                * ((settings.edgeMargin.get() - self.x) / settings.edgeMargin.get())
                * settings.maxSpeed.get()
            )
        elif self.x > CANVASWIDTH - settings.edgeMargin.get():
            self.vx -= (
                settings.turnStrength.get()
                * (
                    (self.x - (CANVASWIDTH - settings.edgeMargin.get()))
                    / settings.edgeMargin.get()
                )
                * settings.maxSpeed.get()
            )

        if self.y < settings.edgeMargin.get():
            self.vy += (
                settings.turnStrength.get()
                * ((settings.edgeMargin.get() - self.y) / settings.edgeMargin.get())
                * settings.maxSpeed.get()
            )
        elif self.y > CANVASHEIGHT - settings.edgeMargin.get():
            self.vy -= (
                settings.turnStrength.get()
                * (
                    (self.y - (CANVASHEIGHT - settings.edgeMargin.get()))
                    / settings.edgeMargin.get()
                )
                * settings.maxSpeed.get()
            )

        speed = math.sqrt(self.vx**2 + self.vy**2)
        adjusted_speed = clamp(settings.minSpeed.get(), speed, settings.maxSpeed.get())

        self.vx *= adjusted_speed / speed
        self.vy *= adjusted_speed / speed

        self.x += self.vx
        self.y += self.vy
        self.x = clamp(0, self.x, CANVASWIDTH)
        self.y = clamp(0, self.y, CANVASHEIGHT)

    def distTo(self, other: "Boid") -> float:
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)


def resetSettings(settings: Settings):
    settings.height.set(BOIDHEIGHT)
    settings.width.set(BOIDWIDTH)
    settings.minSpeed.set(MINSPEED)
    settings.maxSpeed.set(MAXSPEED)
    settings.innerRange.set(INNERRANGE)
    settings.outerRange.set(OUTERRANGE)
    settings.avoidance.set(AVOIDANCE)
    settings.alignment.set(ALIGNMENT)
    settings.centering.set(CENTERING)
    settings.turnStrength.set(TURNSTRENGTH)
    settings.edgeMargin.set(EDGEMARGIN)
    settings.delay.set(DELAY)
    settings.numBoids.set(NUMBOIDS)
    settings.density.set(INITIALDENSITY)


def resetBoids(boids: list["Boid"], settings: Settings):
    cx = CANVASWIDTH / 2
    cy = CANVASHEIGHT / 2
    boids.clear()
    for _ in range(settings.numBoids.get()):
        x = random.randint(
            int(cx - (CANVASWIDTH * 0.5 * (1 - settings.density.get()))),
            int(cx + (CANVASWIDTH * 0.5 * (1 - settings.density.get()))),
        )
        y = random.randint(
            int(cy - (CANVASHEIGHT * 0.5 * (1 - settings.density.get()))),
            int(cy + (CANVASHEIGHT * 0.5 * (1 - settings.density.get()))),
        )
        speed = random.randint(settings.minSpeed.get(), settings.maxSpeed.get())
        direction = random.randint(0, 359)
        vx = speed * math.cos(direction * math.pi / 180)
        vy = speed * math.sin(direction * math.pi / 180)
        boids.append(Boid(x, y, vx, vy))


def clamp(minVal, val, maxVal):
    val = max(minVal, val)
    val = min(val, maxVal)
    return val


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
        speed = random.randint(MINSPEED, MAXSPEED)
        direction = random.randint(0, 359)
        vx = speed * math.cos(direction * math.pi / 180)
        vy = speed * math.sin(direction * math.pi / 180)
        boids.append(Boid(x, y, vx, vy))
    return boids


def main():
    root = tk.Tk()
    root.resizable(False, False)
    canvas = tk.Canvas(root, bg=BG, height=CANVASHEIGHT, width=CANVASWIDTH, bd=0)
    boids = createBoids()
    settings = Settings(root, boids)
    canvas.grid(row=0, column=0, rowspan=12)
    gen = 0
    while True:
        try:
            for boid in boids:
                boid.update(boids, settings)
                boid.draw(canvas, gen, settings)
            canvas.delete("gen" + str(gen - 1))
            gen += 1
            root.after(int(settings.delay.get()))
            root.update()
        except tk.TclError:
            print("Hopefully this means the program exited normally")
            break


if __name__ == "__main__":
    main()
