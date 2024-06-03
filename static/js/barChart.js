function fetchAccountChartData(pk) {
    console.log("Fetching data for account: ", pk)
    let responseData;

    $.ajax({
        url: `/stats/${pk}/account`,
        type: 'GET',
        async: false, // Make the request synchronous
        success: function (response) {
            responseData = response;
        },
        error: function (xhr, status, error) {
            console.error('Error:', status, error);
        }
    });

    return responseData;
}

function createChart(accountID) {
    let accountNoRes = document.getElementById('accountNoRes'); // div with "NO res" text
    let ctx = document.getElementById('accountStatsChart');
    let chartStatus = Chart.getChart("accountStatsChart");
    console.log("Chart Status: ", chartStatus);
    if (chartStatus !== undefined) {
        chartStatus.destroy();
    }
    console.log("Account ID: ", accountID);
    const resp = fetchAccountChartData(accountID);
    if (!resp) {
        accountNoRes.classList.remove('d-none');
        return;
    } else accountNoRes.classList.add('d-none');
    const data = resp.chartData;
    return new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.map(d => d.label),
            datasets: [{
                label: `${resp.username}`,
                data: data.map(d => d.data),
                datalabels: {
                    axis: 'y',
                    align: 'start',
                    anchor: 'end',
                    offset: -20
                },
                backgroundColor: [
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(255, 99, 132, 0.2)',
                ],
                borderColor: [
                    'rgba(54, 162, 235, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(255, 99, 132, 1)',
                ],
                borderWidth: 1
            }]
        },
        options: {
            indexAxis: 'y',
            scales: {
                y: {
                    beginAtZero: true
                }
            },
            responsive: true,
            plugins: {
                datalabels: {
                    color: '#000',
                    display: function (context) {
                        return context.dataset.data[context.dataIndex];
                    }
                },

            legend: {
                    position: 'bottom',
                },
                },
        }
    });
}