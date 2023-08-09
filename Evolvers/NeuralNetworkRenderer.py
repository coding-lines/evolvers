import pygame
import GeneticNN

def get_node_color(value):
    if value > 1:
        return [255, 255, 255]
    if value < -1:
        return [0, 0, 0]

    value = value / 2 + 0.5 #Convert from range [-1, 1] to [0, 1]

    value = round(value * 255) #Convert to color

    return 3 * [value]

def get_text_color(color):
    if sum(color) < 384:
        return [255, 255, 255]
    return [0, 0, 0]

def render_nn(network, dimensions = [1024, 1024], inputs = None, background_color = [0, 0, 0, 0], input_labels = [], output_labels = [], line_width = 1):
    if len(background_color) == 4:
        surface = pygame.Surface(dimensions, pygame.SRCALPHA)
    else:
        surface = pygame.Surface(dimensions)

    surface.fill(background_color)

    col_count = network.layer_count
    col_width = dimensions[0] // network.layer_count
    subcol_width = col_width // 3 #Diameter of node circle, draw circle in subcolumn 2 of 3

    for layer in range(col_count):

        row_count = network.layers[layer]
        row_height = dimensions[1] // row_count
        subrow_height = row_height // 3

        if inputs != None:

            font = pygame.font.Font("font/PTSans-Regular.ttf", subrow_height // 2)

            data = inputs.copy()

            if layer != 0:
                for n_layer in range(layer + 1):
                    data = network.get_layer_output(data, n_layer)

        for node in range(row_count):

            if inputs != None:
                color = get_node_color(data[node])
            else:
                color = (255, 255, 255)

            text_color = get_text_color(color)

            max_size = max(subcol_width, subrow_height)
            size = min(subcol_width, subrow_height)

            x = layer * col_width + subcol_width
            y = node * row_height + subrow_height

            #Proper centering
            if subcol_width > subrow_height:
                x += 0.5 * (max_size - size)
            elif subcol_width < subrow_height:
                y += 0.5 * (max_size - size)

            #Node connections
            if layer + 1 < network.layer_count:
                for n, next_layer_neuron in enumerate(network.neurons[layer + 1]):
                    node_connection = next_layer_neuron.input_weights[node]

                    if node_connection == 0:
                        continue

                    connection_color = get_node_color(node_connection)

                    x1 = x#Start at node base
                    y1 = y

                    next_row_count = network.layers[layer + 1]
                    next_row_height = dimensions[1] // next_row_count
                    next_subrow_height = next_row_height // 3

                    x2 = (layer + 1) * col_width + subcol_width
                    y2 = n * next_row_height + next_subrow_height


                    next_max_size = max(subcol_width, next_subrow_height)
                    next_size = min(subcol_width, next_subrow_height)

                    #Proper centering
                    if subcol_width > next_subrow_height:
                        x2 += 0.5 * (next_max_size - next_size)
                    elif subcol_width < next_subrow_height:
                        y2 += 0.5 * (next_max_size - next_size)

                    pygame.draw.line(surface, connection_color, [x1, y1], [x2, y2], width = line_width)

            pygame.draw.circle(surface, color, [x, y], size // 2)

            if inputs != None:
                node_label = str(round(data[node], 2))
                if node_label.startswith("0."):
                    node_label = node_label[1:]
                elif node_label.startswith("-0."):
                    node_label = "-" + node_label[2:]

                text = font.render(node_label, min(dimensions) > 300, text_color)
                surface.blit(text, [x - text.get_width() // 2, y - text.get_height() // 2])

            if layer == 0 and len(input_labels) > node:
                label_font = pygame.font.Font("font/PTSans-Regular.ttf", subrow_height)
                text = label_font.render(input_labels[node], min(dimensions) > 300, get_text_color(background_color))
                surface.blit(text, [(1.5 * subcol_width - size // 2) // 2 - text.get_width() // 2, y - text.get_height() // 2])
            elif layer == network.layer_count - 1 and len(output_labels) > node:
                label_font = pygame.font.Font("font/PTSans-Regular.ttf", subrow_height // 2)
                text = label_font.render(output_labels[node], min(dimensions) > 300, get_text_color(background_color))
                surface.blit(text, [dimensions[1] - (1.5 * subcol_width - size // 2), y - text.get_height() // 2])

    return surface
