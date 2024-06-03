$(document).ready(
    main
);

async function main() {
    const timelineContainer = document.getElementById('visualization');
    let response = await fetch_timeline_data();
    console.log("response", response)
    console.log(response.groups)
    console.log(response.items)
    let groups = new vis.DataSet(
        response.groups.map(item => {
            return {
                id: item.id,
                content: item.content,
                style: item.style
            }
        })
    );

    let items = new vis.DataSet(
        response.items.map(item => {
            return configureItem(item);
        })
    );
    const currentYear = new Date();
    const startDate = new Date(currentYear.getFullYear(), 0, 1); // January 1st of the current year
    const endDate = new Date(currentYear.getFullYear(), 11, 31);
    let options = {
        autoResize: false,
        zoomMax: 500000000,
        editable: false,

        // always snap to full hours, independent of the scale
        snap: function (date, scale, step) {
            var hour = 60 * 60 * 1000;
            return Math.round(date / hour) * hour;
        }
    }
    let timeline = new vis.Timeline(timelineContainer, items, groups, options);

    $('#parserRunDateTime').daterangepicker({
        "showDropdowns": true,
        "timePicker": true,
        "timePicker24Hour": true,
        "locale": {
            "format": "YYYY/MM/DD (HH:mm) ",
        }
    }, function (start, end, label) {
        let item = {
            id: 3,
            content: "Run Preview",
            start: start,
            end: end,
            group: "worker_1",
            type: "range",
            style: "background-color: var(--bs-success-bg-subtle)"
        }
        items.add(item);
        console.log('New date range selected: ' + start.format('YYYY-MM-DD HH:mm:ss') + ' to ' + end.format('YYYY-MM-DD HH:mm:ss') + ' (predefined range: ' + label + ')');
    });
}

async function fetch_timeline_data() {
    return new Promise((resolve, reject) => {
        $.ajax({
            url: '/timeline/',
            type: 'GET',
            success: function (response) {
                resolve(response);
            },
            error: function (xhr, status, error) {
                reject(error);
            }
        });
    });
}

function configureItem(item) {
    if (new Date(item.start) > new Date()) { // Future runs
        item.style = "background-color: var(--bs-primary-bg-subtle)";
        let content = document.createElement('div')
        content.innerHTML = `
            <i class="bi bi-clock-fill" style="color: var(--bs-dark)"></i> ${item.content}
        `
        item.content = content;
    } else if (new Date(item.end) < new Date()) { // Past runs
        item.style = "background-color: var(--bs-dark-bg-subtle)";
        if (item.status == "failed") {
            let content = document.createElement('div')
            content.innerHTML = `
                <i class="bi bi-exclamation-triangle-fill" style="color: var(--bs-danger)"></i> ${item.content}
            `
            item.content = content;
        } else {
            let content = document.createElement('div')
            content.innerHTML = `
                <i class="bi bi-info-circle-fill" style="color: var(--bs-success)"></i> ${item.content}
            `
            item.content = content;
        }
    } else { // Current runs
        item.style = "background-color: var(--bs-warning-bg-subtle)";
        let content = document.createElement('div')
        content.innerHTML = `
            <div class="spinner-border spinner-border-sm text-secondary"  role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
             ${item.content}
        `
        item.content = content;
    }

    return {
        id: item.id,
        content: item.content,
        start: item.start,
        end: item.end,
        group: item.group,
        style: item.style,
        type: "range",
        editable: false
    }
}