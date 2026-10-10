import os
from datetime import datetime, timedelta

from flask import Flask, request, render_template_string


app = Flask(__name__)


HTML = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>SleepTime — калькулятор сна</title>

    <style>
        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            min-height: 100vh;
            font-family: Arial, sans-serif;
            color: white;
            background:
                radial-gradient(circle at top left, #384b9b 0%, transparent 35%),
                linear-gradient(135deg, #080d2b, #151044 55%, #25145c);
        }

        .container {
            width: 92%;
            max-width: 850px;
            margin: 0 auto;
            padding: 35px 0 50px;
        }

        .header {
            text-align: center;
            margin-bottom: 30px;
        }

        .moon {
            font-size: 58px;
            margin-bottom: 10px;
        }

        h1 {
            margin: 0;
            font-size: 38px;
        }

        .subtitle {
            margin-top: 12px;
            color: #c9cdf5;
            font-size: 17px;
        }

        .card {
            padding: 28px;
            border: 1px solid rgba(255, 255, 255, 0.16);
            border-radius: 24px;
            background: rgba(255, 255, 255, 0.10);
            box-shadow: 0 18px 50px rgba(0, 0, 0, 0.25);
            backdrop-filter: blur(12px);
        }

        .form-title {
            margin-top: 0;
            text-align: center;
            font-size: 23px;
        }

        label {
            display: block;
            margin: 20px 0 8px;
            color: #e0e2ff;
            font-size: 15px;
        }

        input,
        select {
            width: 100%;
            padding: 14px 16px;
            color: white;
            background: rgba(0, 0, 0, 0.25);
            border: 1px solid rgba(255, 255, 255, 0.25);
            border-radius: 12px;
            font-size: 17px;
            outline: none;
        }

        input:focus,
        select:focus {
            border-color: #a9b2ff;
        }

        option {
            color: black;
        }

        button {
            width: 100%;
            margin-top: 25px;
            padding: 15px;
            color: white;
            background: linear-gradient(90deg, #6675ee, #8e5ce6);
            border: none;
            border-radius: 12px;
            font-size: 17px;
            font-weight: bold;
            cursor: pointer;
            transition: 0.2s;
        }

        button:hover {
            transform: translateY(-2px);
            filter: brightness(1.1);
        }

        .result {
            margin-top: 28px;
            padding: 22px;
            border-radius: 18px;
            background: rgba(0, 0, 0, 0.2);
        }

        .result h2 {
            margin-top: 0;
            text-align: center;
            font-size: 22px;
        }

        .time-list {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
            gap: 12px;
            margin-top: 18px;
        }

        .time-item {
            padding: 16px;
            text-align: center;
            border-radius: 14px;
            background: rgba(255, 255, 255, 0.12);
        }

        .time {
            display: block;
            margin-bottom: 5px;
            color: #ffffff;
            font-size: 27px;
            font-weight: bold;
        }

        .cycles {
            color: #cdd1ff;
            font-size: 14px;
        }

        .error {
            margin-top: 20px;
            padding: 14px;
            text-align: center;
            color: #ffd6d6;
            background: rgba(160, 25, 50, 0.4);
            border-radius: 12px;
        }

        .info {
            margin-top: 25px;
            color: #cdd1ff;
            font-size: 14px;
            line-height: 1.6;
            text-align: center;
        }

        footer {
            margin-top: 28px;
            color: #aeb4e8;
            font-size: 13px;
            text-align: center;
        }

        @media (max-width: 600px) {
            .container {
                padding-top: 22px;
            }

            h1 {
                font-size: 30px;
            }

            .card {
                padding: 20px;
            }
        }
    </style>
</head>

<body>
    <main class="container">
        <header class="header">
            <div class="moon">🌙</div>
            <h1>SleepTime</h1>
            <p class="subtitle">
                Рассчитайте лучшее время для отхода ко сну
            </p>
        </header>

        <section class="card">
            <h2 class="form-title">Во сколько вы хотите проснуться?</h2>

            <form method="POST">
                <label for="wake_time">Время пробуждения</label>
                <input
                    type="time"
                    id="wake_time"
                    name="wake_time"
                    value="{{ wake_time }}"
                    required
                >

                <label for="cycles">Количество циклов сна</label>
                <select id="cycles" name="cycles">
                    <option value="4" {% if cycles == 4 %}selected{% endif %}>
                        4 цикла — около 6 часов
                    </option>
                    <option value="5" {% if cycles == 5 %}selected{% endif %}>
                        5 циклов — около 7,5 часов
                    </option>
                    <option value="6" {% if cycles == 6 %}selected{% endif %}>
                        6 циклов — около 9 часов
                    </option>
                </select>

                <button type="submit">
                    Рассчитать время сна
                </button>
            </form>

            {% if result %}
                <div class="result">
                    <h2>Рекомендуемые варианты</h2>

                    <div class="time-list">
                        {% for item in result %}
                            <div class="time-item">
                                <span class="time">{{ item.time }}</span>
                                <span class="cycles">
                                    {{ item.cycles }} циклов сна
                                </span>
                            </div>
                        {% endfor %}
                    </div>
                </div>
            {% endif %}

            {% if error %}
                <div class="error">
                    {{ error }}
                </div>
            {% endif %}

            <p class="info">
                Один цикл сна длится примерно 90 минут.
                Мы также добавляем около 15 минут на засыпание.
            </p>
        </section>

        <footer>
            SleepTime © 2025
        </footer>
    </main>
</body>
</html>
"""


def calculate_sleep_times(wake_time, selected_cycles):
    """
    Возвращает рекомендуемое время отхода ко сну.

    selected_cycles — выбранное пользователем количество циклов.
    Также показываем соседние варианты: на один цикл меньше
    и на один цикл больше.
    """

    wake_datetime = datetime.strptime(wake_time, "%H:%M")

    cycles_to_show = sorted(set([
        selected_cycles - 1,
        selected_cycles,
        selected_cycles + 1
    ]))

    result = []

    for cycles in cycles_to_show:
        if cycles < 3 or cycles > 7:
            continue

        # 90 минут на один цикл + 15 минут на засыпание
        sleep_duration = timedelta(minutes=(cycles * 90) + 15)
        bedtime = wake_datetime - sleep_duration

        result.append({
            "time": bedtime.strftime("%H:%M"),
            "cycles": cycles
        })

    return result


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None

    wake_time = "07:00"
    cycles = 5

    if request.method == "POST":
        wake_time = request.form.get("wake_time", "07:00")
        cycles_text = request.form.get("cycles", "5")

        try:
            cycles = int(cycles_text)

            datetime.strptime(wake_time, "%H:%M")

            if cycles not in [4, 5, 6]:
                raise ValueError

            result = calculate_sleep_times(wake_time, cycles)

        except ValueError:
            error = "Проверьте введённое время и выбранное количество циклов."

    return render_template_string(
        HTML,
        result=result,
        error=error,
        wake_time=wake_time,
        cycles=cycles
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )