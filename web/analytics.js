document.addEventListener('DOMContentLoaded', async function () {
    // Fetch filter options from API and populate dropdowns
    const filtersRes = await fetch('http://localhost:8000/filters');
    const filtersData = await filtersRes.json();

    // Helper to populate a select element
    function populateSelect(id, options) {
        const select = document.getElementById(id);
        select.innerHTML = '';
        options.forEach(opt => {
            const option = document.createElement('option');
            option.value = opt;
            option.textContent = opt;
            select.appendChild(option);
        });
    }

    // populateSelect('timePeriodFilter', filtersData.time_periods);
    populateSelect('segmentFilter', filtersData.segments);
    populateSelect('serviceFilter', filtersData.services);
    populateSelect('contractFilter', filtersData.contracts);

    // Overall Churn Rate Chart
    const churnRateCtx = document.getElementById('churnRateChart').getContext('2d');
    const churnRateChart = new Chart(churnRateCtx, {
        type: 'pie',
        data: {
            labels: [],
            datasets: [{
                data: [],
                backgroundColor: ['#f72585', '#4361ee'],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom'
                },
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            return context.label + ': ' + context.raw + '%';
                        }
                    }
                }
            }
        }
    });

    // Churn Rate by Tenure Chart
    const tenureChurnCtx = document.getElementById('tenureChurnChart').getContext('2d');
    const tenureChurnChart = new Chart(tenureChurnCtx, {
        type: 'line',
        data: {
            labels: [], // 1 to 72 months
            datasets: [{
                label: 'Churn Rate (%)',
                data: [],
                borderColor: '#4361ee',
                backgroundColor: 'rgba(67, 97, 238, 0.1)',
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Tenure (months)'
                    }
                },
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Churn Rate (%)'
                    }
                }
            }
        }
    });

    // Churn by Gender Chart
    const genderChurnCtx = document.getElementById('genderChurnChart').getContext('2d');
    const genderChurnChart = new Chart(genderChurnCtx, {
        type: 'bar',
        data: {
            labels: [],
            datasets: [
                {
                    label: 'Churned',
                    data: [],
                    backgroundColor: '#f72585'
                },
                {
                    label: 'Not Churned',
                    data: [],
                    backgroundColor: '#4361ee'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    stacked: false
                },
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    // Churn by Senior Citizen Status Chart
    const seniorChurnCtx = document.getElementById('seniorChurnChart').getContext('2d');
    const seniorChurnChart = new Chart(seniorChurnCtx, {
        type: 'bar',
        data: {
            labels: [],
            datasets: [
                {
                    label: 'Churned',
                    data: [],
                    backgroundColor: '#f72585'
                },
                {
                    label: 'Not Churned',
                    data: [],
                    backgroundColor: '#4361ee'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });

    // Churn by Partner Status Chart
    const partnerChurnCtx = document.getElementById('partnerChurnChart').getContext('2d');
    const partnerChurnChart = new Chart(partnerChurnCtx, {
        type: 'bar',
        data: {
            labels: [],
            datasets: [
                {
                    label: 'Churned',
                    data: [],
                    backgroundColor: '#f72585'
                },
                {
                    label: 'Not Churned',
                    data: [],
                    backgroundColor: '#4361ee'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: 'Churn Rate by Partnership Status'
                }
            },
            scales: {
                x: {
                    stacked: true, // Enable stacking
                },
                y: {
                    stacked: true,
                    beginAtZero: true,
                    ticks: {
                        callback: function (value) {
                            // This keeps the axis as count, but to show rate, we need to pre-calculate percentages. See note below.
                            return value;
                        }
                    }
                }
            }
        }
    });

    // Churn by Dependents Chart
    const dependentsChurnCtx = document.getElementById('dependentsChurnChart').getContext('2d');
    const dependentsChurnChart = new Chart(dependentsChurnCtx, {
        type: 'bar',
        data: {
            labels: [],
            datasets: [
                {
                    label: 'Churned',
                    data: [],
                    backgroundColor: '#f72585'
                },
                {
                    label: 'Not Churned',
                    data: [],
                    backgroundColor: '#4361ee'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: 'Churn Rate by Dependent Status'
                }
            },
            scales: {
                x: {
                    stacked: true, // Enable stacking
                },
                y: {
                    stacked: true,
                    beginAtZero: true,
                    ticks: {
                        callback: function (value) {
                            // This keeps the axis as count, but to show rate, we need to pre-calculate percentages. See note below.
                            return value;
                        }
                    }
                }
            }
        }
    });

    // Churn by Internet Service Type Chart
    const internetChurnCtx = document.getElementById('internetChurnChart').getContext('2d');
    const internetChurnChart = new Chart(internetChurnCtx, {
        type: 'bar',
        data: {
            labels: [],
            datasets: [
                {
                    label: 'Churned',
                    data: [],
                    backgroundColor: '#f72585'
                },
                {
                    label: 'Not Churned',
                    data: [],
                    backgroundColor: '#4361ee'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });

    // Churn by Contract Type Chart
    const contractChurnCtx = document.getElementById('contractChurnChart').getContext('2d');
    const contractChurnChart = new Chart(contractChurnCtx, {
        type: 'bar',
        data: {
            labels: [],
            datasets: [
                {
                    label: 'Churned',
                    data: [],
                    backgroundColor: '#f72585'
                },
                {
                    label: 'Not Churned',
                    data: [],
                    backgroundColor: '#4361ee'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });

    // Churn by Payment Method Chart
    const paymentChurnCtx = document.getElementById('paymentChurnChart').getContext('2d');
    const paymentChurnChart = new Chart(paymentChurnCtx, {
        type: 'bar',
        data: {
            labels: [],
            datasets: [
                {
                    label: 'Churned',
                    data: [],
                    backgroundColor: '#f72585'
                },
                {
                    label: 'Not Churned',
                    data: [],
                    backgroundColor: '#4361ee'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
        }
    });

    // Churn by Phone Service Chart
    const phoneChurnCtx = document.getElementById('phoneChurnChart').getContext('2d');
    const phoneChurnChart = new Chart(phoneChurnCtx, {
        type: 'bar',
        data: {
            labels: [],
            datasets: [
                {
                    label: 'Churned',
                    data: [],
                    backgroundColor: '#f72585'
                },
                {
                    label: 'Not Churned',
                    data: [],
                    backgroundColor: '#4361ee'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });

    // Monthly Charges Distribution Chart
    const monthlyChargesCtx = document.getElementById('monthlyChargesChart').getContext('2d');
    const monthlyChargesChart = new Chart(monthlyChargesCtx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [
                {
                    label: 'Churned',
                    data: [],
                    backgroundColor: '#f72585'
                },
                {
                    label: 'Not Churned',
                    data: [],
                    backgroundColor: '#4361ee'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Monthly Charges ($)'
                    },
                    ticks: {
                        maxRotation: 45,
                        minRotation: 45
                    }
                },
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Number of Customers'
                    }
                }
            }
        }
    });

    // Total Charges Distribution Chart
    const totalChargesCtx = document.getElementById('totalChargesChart').getContext('2d');
    const totalChargesChart = new Chart(totalChargesCtx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [
                {
                    label: 'Churned',
                    data: [],
                    backgroundColor: '#f72585'
                },
                {
                    label: 'Not Churned',
                    data: [],
                    backgroundColor: '#4361ee'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Total Charges ($)'
                    },
                    ticks: {
                        maxRotation: 45,
                        minRotation: 45
                    }
                },
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Number of Customers'
                    }
                }
            }
        }
    });

    // Churn Rate by Monthly Charges Groups Chart
    const monthlyGroupsChurnCtx = document.getElementById('monthlyGroupsChurnChart').getContext('2d');
    const monthlyGroupsChurnChart = new Chart(monthlyGroupsChurnCtx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Churn Rate (%)',
                data: [],
                backgroundColor: '#178ae96c',
                fill: "start"
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                filler: {
                    propagate: false,
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Monthly Charges Groups ($)'
                    }
                },
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Churn Rate (%)'
                    }
                }
            }
        }
    });

    async function fetchStats(filters) {
        const params = new URLSearchParams(filters).toString();
        const res = await fetch(`http://localhost:8000/stats?${params}`);
        return await res.json();
    }

    async function fetchChart(chartName, filters) {
        const params = new URLSearchParams(filters).toString();
        const res = await fetch(`http://localhost:8000/chart/${chartName}?${params}`);
        return await res.json();
    }

    async function updateDashboard(filters) {
        // Update stats
        const stats = await fetchStats(filters);
        document.querySelector('.stats-value.text-primary').textContent = stats.total_customers;
        document.querySelector('.stats-value.text-warning').textContent = stats.churn_rate + "%";
        document.querySelector('.stats-value.text-info').textContent = "$" + stats.avg_monthly;
        document.querySelector('.stats-value.text-success').textContent = stats.avg_tenure + " mos";

        // Update churn rate chart
        const churnData = await fetchChart("churnRate", filters);
        churnRateChart.data.labels = churnData.labels;
        churnRateChart.data.datasets[0].data = churnData.values;
        churnRateChart.update();

        // Update tenure churn chart
        const tenureData = await fetchChart("tenureChurn", filters);
        tenureChurnChart.data.labels = tenureData.labels;
        tenureChurnChart.data.datasets[0].data = tenureData.values;
        tenureChurnChart.update();

        // Gender Churn Chart
        const genderData = await fetchChart("genderChurn", filters);
        genderChurnChart.data.labels = genderData.labels;
        genderChurnChart.data.datasets[0].data = genderData.churned;
        genderChurnChart.data.datasets[1].data = genderData.not_churned;
        genderChurnChart.update();

        // Senior Citizen Churn Chart
        const seniorData = await fetchChart("seniorChurn", filters);
        seniorChurnChart.data.labels = seniorData.labels;
        seniorChurnChart.data.datasets[0].data = seniorData.churned;
        seniorChurnChart.data.datasets[1].data = seniorData.not_churned;
        seniorChurnChart.update();

        // Partner Churn Chart
        const partnerData = await fetchChart("partnerChurn", filters);
        partnerChurnChart.data.labels = partnerData.labels;
        partnerChurnChart.data.datasets[0].data = partnerData.churned;
        partnerChurnChart.data.datasets[1].data = partnerData.not_churned;
        partnerChurnChart.update();

        // Dependents Churn Chart
        const dependentsData = await fetchChart("dependentsChurn", filters);
        dependentsChurnChart.data.labels = dependentsData.labels;
        dependentsChurnChart.data.datasets[0].data = dependentsData.churned;
        dependentsChurnChart.data.datasets[1].data = dependentsData.not_churned;
        dependentsChurnChart.update();

        // Internet Service Churn Chart
        const internetData = await fetchChart("internetChurn", filters);
        internetChurnChart.data.labels = internetData.labels;
        internetChurnChart.data.datasets[0].data = internetData.churned;
        internetChurnChart.data.datasets[1].data = internetData.not_churned;
        internetChurnChart.update();

        // Contract Type Churn Chart
        const contractData = await fetchChart("contractChurn", filters);
        contractChurnChart.data.labels = contractData.labels;
        contractChurnChart.data.datasets[0].data = contractData.churned;
        contractChurnChart.data.datasets[1].data = contractData.not_churned;
        contractChurnChart.update();

        // Payment Method Churn Chart
        const paymentData = await fetchChart("paymentChurn", filters);
        paymentChurnChart.data.labels = paymentData.labels;
        paymentChurnChart.data.datasets[0].data = paymentData.churned;
        paymentChurnChart.data.datasets[1].data = paymentData.not_churned;
        paymentChurnChart.update();

        // Phone Service Churn Chart
        const phoneData = await fetchChart("phoneChurn", filters);
        phoneChurnChart.data.labels = phoneData.labels;
        phoneChurnChart.data.datasets[0].data = phoneData.churned;
        phoneChurnChart.data.datasets[1].data = phoneData.not_churned;
        phoneChurnChart.update();

        // Monthly Charges Distribution Chart
        const monthlyChargesData = await fetchChart("monthlyChargesDist", filters);
        monthlyChargesChart.data.labels = monthlyChargesData.labels;
        monthlyChargesChart.data.datasets[0].data = monthlyChargesData.churned;
        monthlyChargesChart.data.datasets[1].data = monthlyChargesData.not_churned;
        monthlyChargesChart.update();

        // Total Charges Distribution Chart
        const totalChargesData = await fetchChart("totalChargesDist", filters);
        totalChargesChart.data.labels = totalChargesData.labels;
        totalChargesChart.data.datasets[0].data = totalChargesData.churned;
        totalChargesChart.data.datasets[1].data = totalChargesData.not_churned;
        totalChargesChart.update();

        // Churn Rate by Monthly Charges Groups Chart
        const monthlyGroupsChurnData = await fetchChart("monthlyGroupsChurn", filters);
        monthlyGroupsChurnChart.data.labels = monthlyGroupsChurnData.labels;
        monthlyGroupsChurnChart.data.datasets[0].data = monthlyGroupsChurnData.values;
        monthlyGroupsChurnChart.update();
    }

    document.getElementById('applyFilters').addEventListener('click', function () {
        const filters = {
            // time_period: document.getElementById('timePeriodFilter').value,
            segment: document.getElementById('segmentFilter').value,
            service: document.getElementById('serviceFilter').value,
            contract: document.getElementById('contractFilter').value,
        };
        updateDashboard(filters);
    });

    document.getElementById('resetFilters').addEventListener('click', function () {
        document.getElementById('timePeriodFilter').value = filtersData.time_periods[0];
        document.getElementById('segmentFilter').value = filtersData.segments[0];
        document.getElementById('serviceFilter').value = filtersData.services[0];
        document.getElementById('contractFilter').value = filtersData.contracts[0];
        updateDashboard({
            // time_period: filtersData.time_periods[0],
            segment: filtersData.segments[0],
            service: filtersData.services[0],
            contract: filtersData.contracts[0],
        });
    });

    // Filters collapse logic
    const toggleFiltersBtn = document.getElementById('toggleFiltersBtn');
    const filtersCollapse = document.getElementById('filtersCollapse');
    const toggleFiltersIcon = document.getElementById('toggleFiltersIcon');

    if (toggleFiltersBtn && filtersCollapse && toggleFiltersIcon) {
        toggleFiltersBtn.addEventListener('click', function () {
            if (filtersCollapse.classList.contains('show')) {
                filtersCollapse.classList.remove('show');
                toggleFiltersBtn.setAttribute('aria-expanded', 'false');
                toggleFiltersIcon.classList.remove('fa-chevron-up');
                toggleFiltersIcon.classList.add('fa-chevron-down');
            } else {
                filtersCollapse.classList.add('show');
                toggleFiltersBtn.setAttribute('aria-expanded', 'true');
                toggleFiltersIcon.classList.remove('fa-chevron-down');
                toggleFiltersIcon.classList.add('fa-chevron-up');
            }
        });
    }

    // On page load
    updateDashboard({
        segment: filtersData.segments[0],
        service: filtersData.services[0],
        contract: filtersData.contracts[0],
    });
});