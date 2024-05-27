from PIL import Image, ImageDraw, ImageFont
import math
import discord
from discord.ext import commands
import io

movesHistory = []

def generate_hexagon_vertices(radius, center_x, center_y):
    vertices = []
    for i in range(6):
        angle = math.pi/6 + 2 * math.pi * i / 6  # 60 degrees interval
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        vertices.append((x, y))
    return vertices

def create_hexagonal_board(squareToFill, color):
    size = 40
    width, height = 900, 570
    image = Image.new("RGB", (width, height), (147, 206, 245))
    radius = 30
    centerCoordinates = []
    global movesHistory

    draw = ImageDraw.Draw(image)
    # Draw hexagons, lines, and other game elements here
    start_point = (8, 55)
    end_point = (19+10*15*math.sqrt(3),30+45*11)
    roundedEdgeRadius = 7
    start_box = (start_point[0] - roundedEdgeRadius, start_point[1] - roundedEdgeRadius, start_point[0] + roundedEdgeRadius, start_point[1] + roundedEdgeRadius)
    end_box = (end_point[0] - roundedEdgeRadius, end_point[1] - roundedEdgeRadius, end_point[0] + roundedEdgeRadius, end_point[1] + roundedEdgeRadius)
    draw.ellipse(start_box, fill="orange")
    draw.ellipse(end_box, fill="orange")
    draw.line((start_point[0], start_point[1], end_point[0], end_point[1]), fill = "orange", width = 14)

    startPointOrangeRight = (45+11*30*math.sqrt(3), 55)
    endPointOrangeRight = (56+10*15*math.sqrt(3)+11*30*math.sqrt(3), 30+45*11)
    startBoxOrangeRight = (startPointOrangeRight[0] - roundedEdgeRadius, startPointOrangeRight[1] - roundedEdgeRadius, startPointOrangeRight[0] + roundedEdgeRadius, startPointOrangeRight[1] + roundedEdgeRadius)
    endBoxOrangeRight = (endPointOrangeRight[0] - roundedEdgeRadius, endPointOrangeRight[1] - roundedEdgeRadius, endPointOrangeRight[0] + roundedEdgeRadius, endPointOrangeRight[1] + roundedEdgeRadius)
    draw.ellipse(startBoxOrangeRight, fill="orange")
    draw.ellipse(endBoxOrangeRight, fill="orange")
    draw.line((startPointOrangeRight[0], startPointOrangeRight[1], endPointOrangeRight[0], endPointOrangeRight[1]), fill = "orange", width = 14)

    startPointBrownTop = (30, 20)
    endPointBrownTop = (30 + 11*30*math.sqrt(3), 20)
    startBoxBrownTop = (startPointBrownTop[0] - roundedEdgeRadius, startPointBrownTop[1] - roundedEdgeRadius, startPointBrownTop[0] + roundedEdgeRadius, startPointBrownTop[1] + roundedEdgeRadius)
    endBoxBrownTop = (endPointBrownTop[0] - roundedEdgeRadius, endPointBrownTop[1] - roundedEdgeRadius, endPointBrownTop[0] + roundedEdgeRadius, endPointBrownTop[1] + roundedEdgeRadius)
    draw.ellipse(startBoxBrownTop, fill="brown")
    draw.ellipse(endBoxBrownTop, fill="brown")
    draw.line((startPointBrownTop[0], startPointBrownTop[1], endPointBrownTop[0], endPointBrownTop[1]), fill = "brown", width = 14)

    startPointBrownBottom = (11*15*math.sqrt(3), 55 + 45*11)
    endPointBrownBottom = (30 + 11*45*math.sqrt(3), 55 + 45*11)
    startBoxBrownBottom = (startPointBrownBottom[0] - roundedEdgeRadius, startPointBrownBottom[1] - roundedEdgeRadius, startPointBrownBottom[0] + roundedEdgeRadius, startPointBrownBottom[1] + roundedEdgeRadius)
    endBoxBrownBottom = (endPointBrownBottom[0] - roundedEdgeRadius, endPointBrownBottom[1] - roundedEdgeRadius, endPointBrownBottom[0] + roundedEdgeRadius, endPointBrownBottom[1] + roundedEdgeRadius)
    draw.ellipse(startBoxBrownBottom, fill="brown")
    draw.ellipse(endBoxBrownBottom, fill="brown")
    draw.line((startPointBrownBottom[0], startPointBrownBottom[1], endPointBrownBottom[0], endPointBrownBottom[1]), fill = "brown", width = 14)

    for i in range(0, 11):
        for i2 in range(0, 11):
            if (i == 0):
                font = ImageFont.truetype("arial.ttf", size=10)
                position = (27 + 15*math.sqrt(3) + i2*30*math.sqrt(3), 15)
                text = str(i2+1)
                draw.text(position, text, fill="black", font=font)
            if (i2 == 0):
                font = ImageFont.truetype("arial.ttf", size=10)
                position = (11 + 15*math.sqrt(3)*i, 52 + i*45)
                text = chr(97+i)
                draw.text(position, text, fill="black", font=font)
            currentCoordinate = (30 + i*math.sqrt(3)*radius/2 + math.sqrt(3)*radius/2 + i2*math.sqrt(3)*radius, 30 + radius + i*3/2*radius)
            centerCoordinates.append(currentCoordinate)
            font = ImageFont.truetype("arial.ttf", size=10)
            position = (currentCoordinate[0] -5, currentCoordinate[1]-5)
            text = chr(97+i) + str(i2+1)
            draw.text(position, text, fill="black", font=font)
            currentVertices = generate_hexagon_vertices(radius, currentCoordinate[0], currentCoordinate[1])
            hexagon_points = currentVertices
            for i3 in range(len(hexagon_points)):
                draw.line((hexagon_points[i3], hexagon_points[(i3 + 1) % len(hexagon_points)]), fill="black", width=3)
            if (squareToFill == "new"):
                movesHistory.clear()
            else:
                squareToFillX = ord(squareToFill[0]) - 97
                squareToFillY = int(squareToFill[1:])
                movesHistory.append([squareToFillX, squareToFillY, color])
                for move in movesHistory:
                    if (i == move[0]):
                        if (i2 == move[1]-1):
                            if (move[2] == "brown"):
                                draw.polygon(hexagon_points + [hexagon_points[0]], fill="brown")
                            else:
                                draw.polygon(hexagon_points + [hexagon_points[0]], fill="orange")
                        
    image.save("game_board.png")
    return image

# Example usage:
game_board_image = create_hexagonal_board("new", "orange")
game_board_image.show()  # Display the image locally

intents = discord.Intents.default()
intents.messages = True  # Enable message-related events
intents.message_content = True  # Required to read message content

theColor = "orange"

# Create the bot instance with intents
bot = commands.Bot(command_prefix='!', intents=intents)
@bot.command(name='play')
async def play_game(ctx, *args):
    try:
        theMove = ' '.join(args)
        global theColor
        # Ensure the image creation logic works without error
        game_board_image = create_hexagonal_board(theMove, theColor)
        if (theColor == "orange"):
            theColor = "brown"
        else:
            theColor = "orange"
        
        # Convert the image to an in-memory file
        with io.BytesIO() as image_binary:
            game_board_image.save(image_binary, 'PNG')
            image_binary.seek(0)

            # Send the image file to the Discord channel
            await ctx.send(file=discord.File(fp=image_binary, filename='image.png'))
            print("Image sent successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
        await ctx.send("An error occurred while generating the game board.")

# Run your bot
# bot.run([bot token omitted])
