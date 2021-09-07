let part_number = 1
let question_number = 1
let starting_part_question = 1
let category_name = ""

document.addEventListener('DOMContentLoaded', function () {

    document.querySelectorAll(".results-table").forEach(table => {
        table.style.display = 'none';
    });

    document.querySelectorAll(".expand-collapse").forEach(button => {
        button.addEventListener('click', () => {
            button.classList.toggle("expanded");
            if (button.classList.contains("expanded")){
                button.innerHTML = '<div class="btn-box"><a class="page-link mt-0 px-3">Collapse answers <i class="fa fa-solid fa-chevron-up"></i></a></div>';
                document.querySelector(`#results-${button.value}`).style.display = 'block';
            } else {
                button.innerHTML = '<div class="btn-box"><a class="page-link mt-0 px-3">Expand answers <i class="fa fa-solid fa-chevron-down"></i></a></div>';
                document.querySelector(`#results-${button.value}`).style.display = 'none';
            }

        })
    });

    document.querySelectorAll(".update-score-btn").forEach(button => {
        button.addEventListener('click', () => {
            assignment_id = button.value;
            document.querySelectorAll(`.new-score-${assignment_id}`).forEach(async element => {
                var answer_id = await element.id
                var csrfToken = await document.getElementById("csrfToken").value
                
                await fetch(`/update_score/${assignment_id}/${answer_id}`, {
                    method: 'PUT',
                    headers:{'X-CSRFToken': csrfToken},
                    body: JSON.stringify({
                        new_score: element.value
                    })
                })
            })

        })
    });
})
