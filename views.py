

def check_view(request, pk, question_pk):
    user = request.user
    quiz = Quiz.objects.get(pk=pk)
    question = Question.objects.get(pk=question_pk)
    qs = Answer.objects.filter(question=question)

    # Check wether or not each user has answered the question already
    valid = True
    
    for user in quiz.participants:

        try:
            answer = Answer.objects.get(question=question) 

        except ObjectDoesNotExist:
            valid = False

    if valid:
        
        # Answers received. Therefore review each and reveal the results
        for answer in all_answers:
            answer.review()

        return render(
            request,
             "reveal.html", {
                "all_answers": qs.values_list("char_body", "user", "state"),
                 "correct_answer": question.answer
                 }
        )

    else:

        # Use html for manual refreshement
        return render(request, "wait_for_answers.html", {"answers": qs.values_list("user"), "count": qs.aggregate(count=Count("user"))})


def answer_view(request, pk, quiz_pk):

    ctx = {}
    question = Question.objects.get(pk=pk)
    question_answer = question.answer

    user = request.user
    user_answer = request.GET.get["answer"]
    answer = Answer.objects.create(
        user=user, 
        question=question,
        char_body=user_answer
    )

    # redirect to check view
    return redirect('/wait', quiz_pk)


def question_view(request, pk):
    queston = Question.objects.get(pk=pk)
    return render(request, "question.html", {"question": question})


def quiz_view(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    return render(request, "quiz.html", {"quiz": quiz})

def quiz_result_view(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    ctx = {}

    if quiz.finished():
        ctx["results"] = quiz.get_board()
    else:
        ctx["results"] = None
    
    return render(request, "quiz_results.html", ctx)
    
def quiz_list_view(request):
    return render(request, "quiz_list.html", {"quiz_list": Quiz.objects.all()})