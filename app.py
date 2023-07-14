from flask import Flask, render_template, Markup

app = Flask(__name__)

@app.route('/')
def index():
    # Assuming specialRoomNumber is 'A101'
    specialRoomNumber = 'B202'

    # Example room data
    backendData = {
        'room': 'B202',
        'department': 'Lehrstuhl für Elektrotechnik',
        'department_head': 'Prof. Dr. Dr. Dr. Becker',
        'person': [
            {
                'name': "Prof. Dr. Hans Schmid",
                'degree': "M.Sc"
            },
            {
                'name': "Prof. Dr. Julia Wagne",
                'degree': "Ph.D"
            }
        ],
        'globalRoomNumber': '120.202',
    }
    # More room data...

    svg = open('ercis.svg').read()

    html_string = render_template('index.html', roomData=backendData, specialRoomNumber=specialRoomNumber, svg=Markup(svg))

    print(html_string)

    return html_string

if __name__ == '__main__':
    app.run()
