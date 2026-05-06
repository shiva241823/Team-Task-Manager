// =========================
// CONFIRM DELETE
// =========================

function confirmDelete(
    message = "Are you sure?"
){

    return confirm(message);

}


// =========================
// AUTO HIDE ALERTS
// =========================

document.addEventListener(
    "DOMContentLoaded",
    function(){

        setTimeout(() => {

            const alerts =
                document.querySelectorAll(
                    ".alert"
                );

            alerts.forEach(alert => {

                alert.style.transition =
                    "0.5s ease";

                alert.style.opacity = "0";

                setTimeout(() => {

                    alert.style.display = "none";

                }, 500);

            });

        }, 3000);

    }
);


// =========================
// TASK PROGRESS AUTO STATUS
// =========================

function updateTaskStatus(
    progressInputId,
    statusSelectId
){

    const progressInput =
        document.getElementById(
            progressInputId
        );

    const statusSelect =
        document.getElementById(
            statusSelectId
        );

    if(
        !progressInput ||
        !statusSelect
    ){
        return;
    }

    let progress = parseInt(
        progressInput.value
    );

    if(isNaN(progress)){
        progress = 0;
    }

    // LIMIT VALUES

    if(progress < 0){
        progress = 0;
    }

    if(progress > 100){
        progress = 100;
    }

    progressInput.value = progress;


    // AUTO STATUS

    if(progress === 100){

        statusSelect.value =
            "Completed";

    }
    else if(progress > 0){

        statusSelect.value =
            "In Progress";

    }
    else{

        statusSelect.value =
            "Pending";

    }

}


// =========================
// SEARCH TABLE
// =========================

function searchTable(
    inputId,
    tableId
){

    const input =
        document.getElementById(
            inputId
        );

    const table =
        document.getElementById(
            tableId
        );

    if(
        !input ||
        !table
    ){
        return;
    }

    const filter =
        input.value.toLowerCase();

    const rows =
        table.getElementsByTagName("tr");

    for(let i = 1; i < rows.length; i++){

        const rowText =
            rows[i]
            .textContent
            .toLowerCase();

        if(
            rowText.includes(filter)
        ){

            rows[i].style.display = "";

        }
        else{

            rows[i].style.display = "none";

        }

    }

}


// =========================
// TASK PROGRESS BARS
// =========================

document.addEventListener(
    "DOMContentLoaded",
    function(){

        const progressBars =
            document.querySelectorAll(
                ".progress-bar-fill"
            );

        progressBars.forEach(bar => {

            let progress =
                parseInt(
                    bar.getAttribute(
                        "data-progress"
                    )
                );

            if(isNaN(progress)){
                progress = 0;
            }

            if(progress < 0){
                progress = 0;
            }

            if(progress > 100){
                progress = 100;
            }

            bar.style.width =
                progress + "%";

        });

    }
);


// =========================
// TABLE ROW HOVER EFFECT
// =========================

document.addEventListener(
    "DOMContentLoaded",
    function(){

        const tableRows =
            document.querySelectorAll(
                "table tr"
            );

        tableRows.forEach(row => {

            row.style.transition =
                "0.2s ease";

        });

    }
);


// =========================
// FORM VALIDATION
// =========================

document.addEventListener(
    "DOMContentLoaded",
    function(){

        const forms =
            document.querySelectorAll(
                "form"
            );

        forms.forEach(form => {

            form.addEventListener(
                "submit",
                function(event){

                    const requiredFields =
                        form.querySelectorAll(
                            "[required]"
                        );

                    let valid = true;

                    requiredFields.forEach(field => {

                        // IGNORE HIDDEN FIELDS

                        if(
                            field.offsetParent === null
                        ){
                            return;
                        }

                        if(
                            field.value.trim() === ""
                        ){

                            field.style.border =
                                "1px solid red";

                            valid = false;

                        }
                        else{

                            field.style.border =
                                "1px solid #d1d5db";

                        }

                    });

                    if(!valid){

                        event.preventDefault();

                        alert(
                            "Please fill all required fields."
                        );

                    }

                }
            );

        });

    }
);