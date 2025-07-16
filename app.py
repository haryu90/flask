from flask import Flask, render_template, request, redirect, session, url_for, jsonify
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.permanent_session_lifetime = timedelta(minutes=30)

leaderboard = []

QUESTIONS = [
    # 쉬움
    {
        'type': 'multiple', 'difficulty': 'easy',
        'question': "저는 용돈을 한달에 한번 받습니다. 그런데 이번달에 게임이 너무 많이 나와서 사고 싶은것이 많아졌어요. 이런 상황을 뭐라고 할까요?",
        'choices': ['통장요정', '희소성', '과소비', '경제위기'],
        'answer': '희소성',
        'hint': [
            "희소성 : 자원은 한정되어 있지만, 사람들의 욕구는 무한한 상태.",
            "기회비용 : 어떤 것을 선택하였을 때, 포기하게 되는 다른 선택지의 가치이다.",
            "과소비 : 자신이 가진 자원보다 과하게 지출하는 것이다."
        ],
        'explanation': "자원이 부족한 것 >> 희소성(선택이 필요하다)"
    },
    {
        'type': 'short', 'difficulty': 'easy',
        'question': "수입품의 가격을 인위적으로 높이기 위해 정부가 부과하는 세금은?",
        'answer': '관세',
        'hint': [],
        'explanation': "정답: 관세"
    },
    {
        'type': 'multiple', 'difficulty': 'easy',
        'question': "수요의 가격 탄력성이 높다는 것은, 가격 변화에 따라 수요량이 크게 변한다는 의미다. (O/X)",
        'choices': ['⭕', '❌'],
        'answer': '⭕',
        'hint': [
            "가격이 조금만 올라가도 사람들이 덜 사는 상품이라면, 수요의 가격 탄력성이 크다"
        ],
        'explanation': "수요의 가격 탄력성 개념 확인"
    },
    {
        'type': 'short', 'difficulty': 'easy',
        'question': "국제 무역을 통해 발생하는 ‘서로 이익을 보는 상황’을 경제학적으로 표현하면?",
        'answer': '상호이익',
        'hint': [],
        'explanation': "정답: 상호이익"
    },
    {
        'type': 'short', 'difficulty': 'easy',
        'question': "외국 상품이 국내에 들어오는 것을 무엇이라 하는가?",
        'answer': '수입',
        'hint': [],
        'explanation': "정답: 수입"
    },
    # 보통
    {
        'type': 'multiple', 'difficulty': 'medium',
        'question': "A 회사가 B 회사보다 같은 물건을 더 싸게 잘 만들 수 있어요. 이런 회사를 뭐라고 부를까요?",
        'choices': ['독점회사', '효율회사', '비교우위가 있는 회사', '강자회사'],
        'answer': '비교우위가 있는 회사',
        'hint': [
            "기회비용 : 어떤 선택을 했을 때 포기한 다른 선택의 가치이다.",
            "절대우위 : 더 많은 생산 능력을 지닌 것이다.",
            "비교우위 : 더 낮은 기회비용으로 생산할 수 있는 능력.",
            "독점회사 : 시장을 하나의 회사가 지배하는 것으로 가격 경쟁사가 없다."
        ],
        'explanation': "비교우위: 더 적은 비용으로 더 잘할 수 있는 능력"
    },
    {
        'type': 'multiple', 'difficulty': 'medium',
        'question': "회사가 광고에 돈을 많이 써서 고객이 갑자기 2배로 늘었어요. 이때 필요한 것은?",
        'choices': ['더 큰 사무실', '더 많은 재고', '더 많은 세금', '전기 요금 할인'],
        'answer': '더 많은 재고',
        'hint': [
            "수요 증가 : 상품이나 서비스를 구매하려는 사람의 수나 의지가 증가하는 것이다.",
            "세금 : 수익이 발생한 뒤 발생하는 결과.",
            "재고의 중요성 : 판매할 상품을 미리 확보해두는 것이 중요.",
            "수요와 공급의 법칙 : 수요가 늘면 가격이 오르고, 공급이 늘면 가격이 내리는 것."
        ],
        'explanation': "수요가 늘면 공급도 따라줘야 한다 (더 많은 재고 필요)"
    },
    # 어려움
    {
        'type': 'multiple', 'difficulty': 'hard',
        'question': "중앙은행이 금리를 올리면, 사람들의 소비는 어떻게 될 가능성이 높을까요?",
        'choices': ['늘어난다', '줄어든다', '변하지 않는다', '대출이 쉬워진다'],
        'answer': '줄어든다',
        'hint': [
            "금리 : 돈을 빌릴 때 내야하는 이자의 비율.",
            "중앙은행 : 한 나라의 금융을 조절하고, 경제를 안정시키는 기관."
        ],
        'explanation': "금리가 올라가면 대출이 비싸지고 소비가 줄어드는 경향"
    },
    {
        'type': 'multiple', 'difficulty': 'hard',
        'question': "경기 침체가 계속되면 정부는 어떤 조치를 취할 수 있을까요?",
        'choices': ['금리를 올린다', '세금을 줄이고 정부 지출을 늘린다', '수출을 금지한다', '주식을 매입한다'],
        'answer': '세금을 줄이고 정부 지출을 늘린다',
        'hint': ["경기 침체 : 나라 전체의 경제활동이 위축되는 상태"],
        'explanation': "재정 정책을 통해 정부는 경기 부양을 시도함"
    },
    {
        'type': 'multiple', 'difficulty': 'hard',
        'question': "다음 중 ‘GDP(국내 총생산)’의 정의로 가장 올바른 것은?",
        'choices': [
            '한 나라 국민이 1년간 국내 외에서 벌어들인 소득의 총합',
            '정부가 1년간 사용하는 예산 총액',
            '한 나라에서 일정기간 동안 생산된 모든 최종재화와 서비스의 시장가치',
            '시중에 유통되는 총통화량에서 외환 보유고를 제외한 금액'
        ],
        'answer': '한 나라에서 일정기간 동안 생산된 모든 최종재화와 서비스의 시장가치',
        'hint': [
            "GDP의 예시: 쌍문동 편의점에서 판매한 음식, 삼성전자가 만든 갤럭시폰",
            "GDP가 중요한 이유: 경제 크기와 활발함을 알 수 있음"
        ],
        'explanation': "정확한 GDP 정의이며, 국내 최종 재화와 서비스의 시장가치를 합산한 수치"
    }
]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session['nickname'] = request.form['nickname']
        session['score'] = 0
        session['stock'] = 0.0
        session['correct'] = 0
        session['wrong'] = 0
        session['used_hint'] = False
        return redirect(url_for('loading'))
    return render_template('index.html')

@app.route('/loading')
def loading():
    return render_template('loading.html')

@app.route('/game')
def game():
    return render_template('game.html')

@app.route('/questions')
def get_questions():
    return jsonify(QUESTIONS)

@app.route('/submit_result', methods=['POST'])
def submit_result():
    data = request.json
    nickname = session.get('nickname', '플레이어')
    stock = data.get('stock', 0)
    correct = data.get('correct', 0)
    wrong = data.get('wrong', 0)
    leaderboard.append({
        'nickname': nickname,
        'stock': stock,
        'correct': correct,
        'wrong': wrong
    })
    leaderboard.sort(key=lambda x: x['stock'], reverse=True)
    session['final'] = {
        'stock': stock,
        'correct': correct,
        'wrong': wrong
    }
    return jsonify(success=True)

@app.route('/reset')
def reset():
    session.clear()
    return redirect(url_for('index'))

@app.route('/clear_leaderboard')
def clear_leaderboard():
    leaderboard.clear()
    return redirect(url_for('result'))


@app.route('/result')
def result():
    nickname = session.get('nickname')
    final = session.get('final', {})

    if not nickname or not final:
        return redirect(url_for('index'))

    final.setdefault('stock', 0)
    final.setdefault('correct', 0)
    final.setdefault('wrong', 0)

    rank = 0
    for i, user in enumerate(leaderboard):
        if user['nickname'] == nickname and user['stock'] == final.get('stock'):
            rank = i + 1
            break

    return render_template('result.html', leaderboard=leaderboard, your_rank=rank, nickname=nickname, result=final)

@app.route('/leaderboard_all')
def leaderboard_all():
    nickname = session.get('nickname')
    if not nickname:
        return redirect(url_for('index'))
    return render_template('leaderboard.html', leaderboard=leaderboard)



import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

