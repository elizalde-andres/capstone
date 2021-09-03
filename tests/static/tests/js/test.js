let part_number = 1
let question_number = 1
let starting_part_question = 1
let category_name = ""

document.addEventListener('DOMContentLoaded', function () {
    try{
        load_form()
        edit_btn = document.querySelector("#edit-btn")
        edit_btn.addEventListener("click", () => {
            edit_btn.style.display = "none"
            edit_test(edit_btn.value)
        })
    } catch(err) {
    }
    try{
        next_part_btn = document.querySelector("#next-part-button")
        assignment_id = document.querySelector("#assignment-id").value
        next_part_btn.addEventListener("click", () => save_current_answers(assignment_id, false))
    }catch(err){
    }try{
        prev_part_btn = document.querySelector("#prev-part-button")
        assignment_id = document.querySelector("#assignment-id").value
        prev_part_btn.addEventListener("click", () => save_current_answers(assignment_id, false))
    }catch(err){
    }
    try{
        finish_btn = document.querySelector("#finish-button")
        assignment_id = document.querySelector("#assignment-id").value
        finish_btn.addEventListener("click", () => save_current_answers(assignment_id, true))
    }catch(err){
    }
    
     
})

async function load_form() {
    try{
        new_test_form = await fetch('/abm_test_layout')
        new_test_form = await new_test_form.text()
        
        
        await (document.querySelector("#test-form").innerHTML = new_test_form)

        category = document.querySelector("#test-category > select")
        
        category.addEventListener("change",() => {
            document.querySelector("#parts-forms").innerHTML = ""
            if (category.options[category.selectedIndex].text != ""){
                category_name = category.options[category.selectedIndex].text
                add_empty_part_form();
            }
        })
    } catch(err) {
    }

}

async function add_empty_part_form() {
    part_forms = document.querySelector("#parts-forms");

    new_part_form = await fetch('/abm_testpart_layout?' + new URLSearchParams({
        category: category_name,
        part_number: part_number
    }))
    new_part_form = await new_part_form.text();

    await (part_forms.insertAdjacentHTML("beforeend", new_part_form));

    document.querySelector(`#add-part-btn-${part_number}`).addEventListener("click", () => add_new_part())
    
    await add_empty_question_form();
}

async function add_new_part() {
    document.querySelector(`#add-question-${question_number}`).style.display = "none"
    document.querySelector(`#delete-question-${question_number}`).style.display = "none"
    document.querySelector(`#add-part-btn-${part_number}`).style.display = "none"

    question_number += 1
    starting_part_question = question_number
    part_number += 1
    await add_empty_part_form()
}

async function add_empty_question_form() {
    question_forms = document.querySelector(`#question-forms-${part_number}`)

    new_question_form = await fetch('/abm_question_layout?' + new URLSearchParams({
        category: category_name,
        question_number: question_number,
        part_number: part_number
    }))
    new_question_form = await new_question_form.text();

    await (question_forms.insertAdjacentHTML("beforeend",new_question_form));

    if (question_number == starting_part_question) {
        document.querySelector(`#delete-question-${question_number}`).style.display = "none"
    }

    document.querySelector(`#add-question-${question_number}`).addEventListener("click", () => add_new_question())

    document.querySelector(`#delete-question-${question_number}`).addEventListener("click", function () {
        document.querySelector(`#question-form-${part_number}-${question_number}`).remove();
        question_number -= 1;
        document.querySelector(`#add-question-${question_number}`).style.display = "inline"
        if (question_number != starting_part_question) {
            document.querySelector(`#delete-question-${question_number}`).style.display = "inline"
        }
    })
}

async function add_new_question() {
    document.querySelector(`#add-question-${question_number}`).style.display = "none"
    document.querySelector(`#delete-question-${question_number}`).style.display = "none"
    question_number += 1
    await add_empty_question_form();
}


async function edit_test(id) {

    test_data = await fetch('/get_test?' + new URLSearchParams({
        id: id
    }))
    test_data = await test_data.json();

    category_name = test_data.category_name
    console.log(test_data)

    document.querySelector("#view-test-section").style.display = 'none';
    document.querySelector("#edit-test-view").innerHTML = '<div id="test-form"></div>';

    await load_form();
    document.querySelector("#form-title").innerHTML = "Edit test"
    document.querySelector("#main-form").action = `/edit_test/${id}`
    document.querySelector("#confirm-button").innerHTML = "Save"

    input_title = document.querySelector("#test-form-title > input")
    input_title.value = test_data.title

    select_category = document.querySelector("#test-category > select")
    select_category.value = test_data.category_id
    select_category.setAttribute("disabled", "disabled")

    // Create Part 1 and its questions forms
    await add_empty_part_form()

    current_question_answers = test_data.parts[part_number-1].questions[question_number-1].correct_answers
    document.querySelector(`#correct-answers-${part_number}-${question_number}`).value = current_question_answers
    
    for (var i = 1; i < Object.keys(test_data.parts[0].questions).length; i++) {
        await add_new_question()
        current_question_answers = test_data.parts[part_number-1].questions[question_number-1].correct_answers
        document.querySelector(`#correct-answers-${part_number}-${question_number}`).value = current_question_answers
    }

    // Create Parts 2, 3, ... and its questions forms
    for (var i = 1; i < Object.keys(test_data.parts).length; i++) {
        await add_new_part()
        for (var j = 1; j < Object.keys(test_data.parts[part_number-1].questions).length; j++) {
            await add_new_question()
            current_question_answers = test_data.parts[part_number-1].questions[question_number-1-starting_part_question].correct_answers
            document.querySelector(`#correct-answers-${part_number}-${question_number-1}`).value = current_question_answers
        }
        current_question_answers = test_data.parts[part_number-1].questions[question_number-starting_part_question].correct_answers
        document.querySelector(`#correct-answers-${part_number}-${question_number}`).value = current_question_answers
    }

    // Fill parts data
    for (var i = 0; i < part_number; i++) {
        document.querySelector(`#text-content-${i+1}`).value = test_data.parts[i].content
        document.querySelector(`#is-multiple-choice-${i+1}`).checked = test_data.parts[i].is_multiple_choice
        document.querySelector(`#max-score-per-answer-${i+1}`).value = test_data.parts[i].max_score_per_answer 
    }

    // Hide unwanted buttons
    document.querySelector(`#add-part-btn-${part_number}`).style.display = "none"
    document.querySelector(`#add-question-${question_number}`).style.display = "none"
    document.querySelector(`#delete-question-${question_number}`).style.display = "none"

}

async function save_current_answers(assignment_id, finish) {
    part_num = document.querySelector("#part-number").value
    answers = {}

    question_numbers = document.querySelectorAll(".question_number")
    question_numbers.forEach(question_num => {
        answers[question_num.innerHTML] = document.querySelector(`#answer-${question_num.innerHTML}`).value
    })
    console.log(answers)
    await fetch(`/answer/${assignment_id}`, {
        method: 'PUT',
        headers:{'X-CSRFToken': getCookie("csrftoken")},
        body: JSON.stringify({
            finish: finish,
            part_number: part_num,
            answers: answers
        })
      })
}
// TODO: Preload answers if test is not finished

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
  }