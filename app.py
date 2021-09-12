from flask import Flask, render_template, url_for, flash
from werkzeug.utils import redirect
# from werkzeug.wrappers import request
from project.forms import Config, MessageForm, House, LevelForm

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/', methods=['get', 'post'])
@app.route('/index', methods=['get', 'post'])
def index():
    player = House()
    form=LevelForm()
    if form.validate_on_submit():
        player.restart()
        player.counter = 5 * (form.level.data)
        return redirect('/maze:start')
    return render_template('index.html', form=form)


@app.route('/maze:<status>', methods=['get', 'post'])
def maze(status):
    if status == 'gameover':
        return render_template('gameover.html')

    if status == 'youwin':
        return render_template('youwin.html')

    form = MessageForm()
    player = House()
    if form.validate_on_submit():
        way = form.way.data
        step = form.number_steps.data
        method = (player.up, player.right, player.down, player.left)[way]
        for _ in range(step):
            player.counter -= 1
            res = method(1)
            if res == '':
                flash(f'Вы находетесь в "{player.room}"', 'alert alert-primary')
            else:
                if res == 'Вы победили':
                    return redirect('/maze:youwin')
                #     flash(res, 'alert alert-info')
                #     break
                else:
                    flash(res, 'alert alert-warning')
            if player.counter < 0:
                return redirect('/maze:gameover')
        link_map = f'img/{player.x}_{player.y}.png'
        return render_template('maze.html', form=form, link_map=link_map, counter=player.counter)

    
    flash('Вчерашний поход к барону явно удался. Сейчас Вы в пыльной комнате и Ваше самочуствие после бурной ночи оставляет желать лучшего. Глоток свежего воздуха - вот лучшее решение. Пора пробираться к балкону.', 'alert alert-info')
    link_map = f'img/{player.x}_{player.y}.png'
    return render_template('maze.html', form=form, link_map=link_map, counter=player.counter)


if __name__ == '__main__':
    app.run(debug=True)
