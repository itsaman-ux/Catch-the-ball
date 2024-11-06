import tkinter as tk
import random

class CatchTheBallGame:
    def __init__(self, root):  # Changed _init_ to __init__
        self.root = root
        self.root.title("Catch the Ball - Level Edition")
        
        self.canvas_width = 400
        self.canvas_height = 400
        self.paddle_width = 80
        self.paddle_height = 15
        self.ball_radius = 10
        self.paddle_speed = 20
        self.score = 0
        self.high_score = 0
        self.level = 1
        self.score_to_next_level = 5
        self.game_over = False

        self.level_colors = [
            {"bg": "black", "paddle": "blue", "ball": "red"},
            {"bg": "navy", "paddle": "green", "ball": "yellow"},
            {"bg": "darkgreen", "paddle": "purple", "ball": "orange"},
            {"bg": "darkred", "paddle": "cyan", "ball": "pink"},
        ]

        self.canvas = tk.Canvas(root, width=self.canvas_width, height=self.canvas_height, bg=self.level_colors[0]["bg"])
        self.canvas.pack()

        self.paddle = self.canvas.create_rectangle(
            (self.canvas_width - self.paddle_width) // 2, self.canvas_height - 30,
            (self.canvas_width + self.paddle_width) // 2, self.canvas_height - 30 + self.paddle_height,
            fill=self.level_colors[0]["paddle"]
        )

        self.ball = self.canvas.create_oval(0, 0, self.ball_radius * 2, self.ball_radius * 2, fill=self.level_colors[0]["ball"])
        self.ball_speed = 5
        self.reset_ball()

        self.score_text = self.canvas.create_text(50, 20, text="Score: 0", fill="white", font=("Arial", 14))
        self.high_score_text = self.canvas.create_text(350, 20, text=f"High Score: {self.high_score}", fill="white", font=("Arial", 14))
        self.level_text = self.canvas.create_text(200, 20, text="Level: 1", fill="white", font=("Arial", 14))

        self.root.bind("<Left>", self.move_paddle_left)
        self.root.bind("<Right>", self.move_paddle_right)

        self.update_game()

    def reset_ball(self):
        x = random.randint(0, self.canvas_width - self.ball_radius * 2)
        self.canvas.coords(self.ball, x, 0, x + self.ball_radius * 2, self.ball_radius * 2)
        self.ball_dy = self.ball_speed

    def move_paddle_left(self, event):
        if not self.game_over:
            self.canvas.move(self.paddle, -self.paddle_speed, 0)
            if self.canvas.coords(self.paddle)[0] < 0:
                self.canvas.move(self.paddle, -self.canvas.coords(self.paddle)[0], 0)

    def move_paddle_right(self, event):
        if not self.game_over:
            self.canvas.move(self.paddle, self.paddle_speed, 0)
            if self.canvas.coords(self.paddle)[2] > self.canvas_width:
                self.canvas.move(self.paddle, self.canvas_width - self.canvas.coords(self.paddle)[2], 0)

    def update_game(self):
        if not self.game_over:
            self.canvas.move(self.ball, 0, self.ball_dy)
            paddle_coords = self.canvas.coords(self.paddle)
            ball_coords = self.canvas.coords(self.ball)
            
            if (paddle_coords[1] <= ball_coords[3] <= paddle_coords[3] and 
                paddle_coords[0] < ball_coords[2] and paddle_coords[2] > ball_coords[0]):
                self.score += 1
                self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")
                self.reset_ball()
                self.check_for_level_up()
            elif ball_coords[3] >= self.canvas_height:
                self.end_game()

            self.root.after(50, self.update_game)

    def check_for_level_up(self):
        if self.score >= self.score_to_next_level * self.level:
            self.level += 1
            self.ball_speed += 2
            self.update_level()

    def update_level(self):
        if self.level - 1 < len(self.level_colors):
            color_scheme = self.level_colors[self.level - 1]
            self.canvas.config(bg=color_scheme["bg"])
            self.canvas.itemconfig(self.paddle, fill=color_scheme["paddle"])
            self.canvas.itemconfig(self.ball, fill=color_scheme["ball"])
        self.canvas.itemconfig(self.level_text, text=f"Level: {self.level}")

    def end_game(self):
        self.game_over = True
        if self.score > self.high_score:
            self.high_score = self.score
            self.canvas.itemconfig(self.high_score_text, text=f"High Score: {self.high_score}")
        self.canvas.create_text(self.canvas_width / 2, self.canvas_height / 2, text="Game Over", fill="white", font=("Arial", 24))
        self.canvas.create_text(self.canvas_width / 2, self.canvas_height / 2 + 30, text="Press R to Restart", fill="white", font=("Arial", 16))
        self.root.bind("<r>", self.restart_game)

    def restart_game(self, event):
        self.canvas.delete("all")
        self.__init__(self.root)  # Call __init__ instead of _init_

root = tk.Tk()
game = CatchTheBallGame(root)
root.mainloop()
