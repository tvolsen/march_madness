from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import pandas as pd
year = 2022

games = pd.read_csv(f"brackets/{year}-bracket.csv")
regions = games[-1:]
regions = list(regions.iloc[0])[:-1]
games = games[:-1]
positions = ["top left", "bottom left", "top right", "bottom right"]
games["prediction"] = games["winner"]

def add_image(image_path):
    c = canvas.Canvas("predictions/test.pdf", pagesize=letter)
    c.drawImage(image_path, 6, -10, width=600, height=800)
    c.setFontSize(16)
    c.drawString(190, 770, f"{year}")
    c.setFontSize(6)
    c.drawString(260, 760, "(higher seed is always on the top)")
    c.setFillColorRGB(1, 0, 0)
    c.setFillColorRGB(0, 1, 0)
    c.setFontSize(7)

    text_alignment = {
        "left" : c.drawRightString,
        "right" : c.drawString
    }

    text_location = {
        "left" : lambda x: x+64,
        "right" : lambda x: x
    }

    y_drop = {
        1 : 30.5,
        2 : 61,
        3 : 123,
        4 : 0
    }

    team1_drop = {
        1 : 17,
        2 : 17,
        3 : 45,
        4 : 105
    }

    def draw_round(x, y, dir, df, round):
        df = df[df["round"] == round]
        df = list(zip(df["team0"], df["team1"], df["winner"], df["prediction"]))
        c.setFontSize(7)
        if round < 5:
            for i in range(8 // 2**(round-1)):
                team0, team1, winner, prediction = df.pop(0)
                if team0 == winner and prediction == team0:
                    c.setFillColorRGB(0, 1, 0)
                    text_alignment[dir](text_location[dir](x), y, team0[:18])
                elif team0 == winner and prediction != team0:
                    c.setFillColorRGB(1, 0, 0)
                    text_alignment[dir](text_location[dir](x), y, team0[:18])
                else:
                    c.setFillColorRGB(0, 0, 0)
                    text_alignment[dir](text_location[dir](x), y, team0[:18])
                if team1 == winner and prediction == team1:
                    c.setFillColorRGB(0, 1, 0)
                    text_alignment[dir](text_location[dir](x), y-team1_drop[round], team1[:18])
                elif team1 == winner and prediction != team1:
                    c.setFillColorRGB(1, 0, 0)
                    text_alignment[dir](text_location[dir](x), y-team1_drop[round], team1[:18])
                else:
                    c.setFillColorRGB(0, 0, 0)
                    text_alignment[dir](text_location[dir](x), y-team1_drop[round], team1[:18])  
                y -= y_drop[round]

    def draw_region(name, position, games):
        df = games[games["region"] == name]            
        if position == "top left":
            # draw the region name
            c.setFontSize(20)
            c.setFillColorRGB(0, 0, 0)
            c.drawCentredString(160, 683, name)

            # draw the teams
            draw_round(20, 655, "left", df, 1)
            draw_round(90, 640, "left", df, 2)
            draw_round(160, 625, "left", df, 3)
            draw_round(230, 595, "left", df, 4)
        elif position == "bottom left":
            # bottom left
            c.setFontSize(20)
            c.setFillColorRGB(0, 0, 0)
            c.drawCentredString(160, 50, name)
            draw_round(20, 318, "left", df, 1)
            draw_round(90, 303, "left", df, 2)
            draw_round(160, 288, "left", df, 3)
            draw_round(230, 258, "left", df, 4)
        elif position == "top right":
            # top right
            c.setFontSize(20)
            c.setFillColorRGB(0, 0, 0)
            c.drawCentredString(452, 683, name)
            draw_round(528, 655, "right", df, 1)
            draw_round(458, 640, "right", df, 2)
            draw_round(388, 625, "right", df, 3)
            draw_round(318, 595, "right", df, 4)
        elif position == "bottom right":
            #bottom right
            c.setFontSize(20)
            c.drawCentredString(452, 50, name)
            draw_round(528, 318, "right", df, 1)
            draw_round(458, 303, "right", df, 2)
            draw_round(388, 288, "right", df, 3)
            draw_round(318, 258, "right", df, 4)
        else:
            print("Invalid position")
            exit(1)

    def draw_finals(games):
        df = games[games["round"] == 5]
        df = list(zip(df["team0"], df["team1"], df["winner"], df["prediction"]))
        team0, team1, winner, prediction = df.pop(0)
        if team0 == winner and prediction == team0:
            c.setFillColorRGB(0, 1, 0)
            c.drawRightString(255, 395, team0[:18])
        elif team0 == winner and prediction != team0:
            c.setFillColorRGB(1, 0, 0)
            c.drawRightString(255, 395, team0[:18])
        else:
            c.setFillColorRGB(0, 0, 0)
            c.drawRightString(255, 395, team0[:18])
        if team1 == winner and prediction == team1:
            c.setFillColorRGB(0, 1, 0)
            c.drawRightString(255, 350, team1[:18])
        elif team1 == winner and prediction != team1:
            c.setFillColorRGB(1, 0, 0)
            c.drawRightString(255, 350, team1[:18])
        else:
            c.setFillColorRGB(0, 0, 0)
            c.drawRightString(255, 350, team1[:18]) 

        team0, team1, winner, prediction = df.pop(0)
        if team0 == winner and prediction == team0:
            c.setFillColorRGB(0, 1, 0)
            c.drawString(351, 395, team0[:18])
        elif team0 == winner and prediction != team0:
            c.setFillColorRGB(1, 0, 0)
            c.drawString(351, 395, team0[:18])
        else:
            c.setFillColorRGB(0, 0, 0)
            c.drawString(351, 395, team0[:18])
        if team1 == winner and prediction == team1:
            c.setFillColorRGB(0, 1, 0)
            c.drawString(351, 350, team1[:18])
        elif team1 == winner and prediction != team1:
            c.setFillColorRGB(1, 0, 0)
            c.drawString(351, 350, team1[:18])
        else:
            c.setFillColorRGB(0, 0, 0)
            c.drawString(351, 350, team1[:18])


        df = games[games["round"] == 6]
        df = list(zip(df["team0"], df["team1"], df["winner"], df["prediction"]))
        team0, team1, winner, prediction = df.pop(0)
        if team0 == winner and prediction == team0:
            c.setFillColorRGB(0, 1, 0)
            c.drawString(259, 377, team0[:18])
        elif team0 == winner and prediction != team0:
            c.setFillColorRGB(1, 0, 0)
            c.drawString(259, 377, team0[:18])
        else:
            c.setFillColorRGB(0, 0, 0)
            c.drawString(259, 377, team0[:18])
        if team1 == winner and prediction == team1:
            c.setFillColorRGB(0, 1, 0)
            c.drawRightString(347, 370, team1[:18])
        elif team1 == winner and prediction != team1:
            c.setFillColorRGB(1, 0, 0)
            c.drawRightString(347, 370, team1[:18])
        else:
            c.setFillColorRGB(0, 0, 0)
            c.drawRightString(347, 370, team1[:18])
            
        if winner == prediction:
            c.setFillColorRGB(0, 1, 0)
            c.drawCentredString(303, 400, prediction)
        else:
            c.setFillColorRGB(1, 0, 0)
            c.drawCentredString(303, 400, prediction)

    for name, position in zip(regions, positions):
        draw_region(name, position, games)
    draw_finals(games)

    c.save()
    
if __name__ == '__main__':
    image_path = 'predictions/empty-bracket.png'
    add_image(image_path)