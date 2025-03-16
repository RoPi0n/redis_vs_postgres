const canvas = document.getElementById('perfomance-chart');
var chart = null;
var chart_datasets = [];


function on_resize_handler(event) {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    if(chart != null) {
        chart.resize(window.innerWidth, window.innerHeight - 20);
    }
}


window.onresize = on_resize_handler;


fetch('/test/redis').then( (resp) => {
    resp.json().then( (results_redis) => {
        
        chart_datasets = [
            {
                label: `Redis Insert (${results_redis.redis_insert_total} ms)`,
                data: Object.keys(results_redis.redis_insert).map(key => {
                    return {
                        x: key / 1000,
                        y: results_redis.redis_insert[key] / 1000,
                        r: 2
                    }
                }),
                backgroundColor: 'rgb(255, 0, 0)'
            },

            {
                label: `Redis Update (${results_redis.redis_update_total} ms)`,
                data: Object.keys(results_redis.redis_update).map(key => {
                    return {
                        x: key / 1000,
                        y: results_redis.redis_update[key] / 1000,
                        r: 2
                    }
                }),
                backgroundColor: 'rgb(255, 166, 0)'
            },

            {
                label: `Redis Get (${results_redis.redis_get_total} ms)`,
                data: Object.keys(results_redis.redis_get).map(key => {
                    return {
                        x: key / 1000,
                        y: results_redis.redis_get[key] / 1000,
                        r: 2
                    }
                }),
                backgroundColor: 'rgb(255, 0, 255)'
            },

            {
                label: `Redis Get by mask (${results_redis.redis_get_m_total} ms)`,
                data: Object.keys(results_redis.redis_get_m).map(key => {
                    return {
                        x: key / 1000,
                        y: results_redis.redis_get_m[key] / 1000,
                        r: 2
                    }
                }),
                backgroundColor: 'rgb(44, 69, 90)'
            }
        ];

        chart = new Chart(canvas, {
            type: 'bubble',
            data: {
                datasets: chart_datasets
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'chartArea',
                        align: 'end',
                        labels: {
                            boxWidth: 20,
                            boxHeight: 20,
                            font: {
                                size: 20
                            }
                        }
                    }
                }
            }
        });


        fetch('/test/postgres').then( (resp) => {
            resp.json().then( (results_pg) => {
                
                chart_datasets.push(
                    {
                        label: `PG Insert (${results_pg.pg_insert_total} ms)`,
                        data: Object.keys(results_pg.pg_insert).map(key => {
                            return {
                                x: key / 1000,
                                y: results_pg.pg_insert[key] / 1000,
                                r: 2
                            }
                        }),
                        backgroundColor: 'rgb(4, 0, 255)'
                    }
                );

                chart_datasets.push(
                    {
                        label: `PG Update (${results_pg.pg_update_total} ms)`,
                        data: Object.keys(results_pg.pg_update).map(key => {
                            return {
                                x: key / 1000,
                                y: results_pg.pg_update[key] / 1000,
                                r: 2
                            }
                        }),
                        backgroundColor: 'rgb(16, 131, 16)'
                    }
                );

                chart_datasets.push(
                    {
                        label: `PG Select (${results_pg.pg_select_total} ms)`,
                        data: Object.keys(results_pg.pg_select).map(key => {
                            return {
                                x: key / 1000,
                                y: results_pg.pg_select[key] / 1000,
                                r: 2
                            }
                        }),
                        backgroundColor: 'rgb(0, 0, 0)'
                    }
                );

                /*chart_datasets.push(
                    {
                        label: `PG Select by mask (${results_pg.pg_select_m_total} ms)`,
                        data: Object.keys(results_pg.pg_select_m).map(key => {
                            return {
                                x: key,
                                y: results_pg.pg_select_m[key] / 1000,
                                r: 2
                            }
                        }),
                        backgroundColor: 'rgb(78, 59, 59)'
                    }
                );*/
        
                if(chart != null) {
                    chart.destroy();
                }

                chart = new Chart(canvas, {
                    type: 'bubble',
                    data: {
                        datasets: chart_datasets
                    },
                    options: {
                        responsive: true,
                        plugins: {
                            legend: {
                                position: 'chartArea',
                                align: 'end',
                                labels: {
                                    boxWidth: 20,
                                    boxHeight: 20,
                                    font: {
                                        size: 20
                                    }
                                }
                            }
                        }
                    }
                });
        
            }).catch( (err) => {
                console.error('Fetch data parsing error!');
                console.error(err);
            });
        }).catch( (err) => {
            console.error('Fetch error!');
            console.error(err);
        });


    }).catch( (err) => {
        console.error('Fetch data parsing error!');
        console.error(err);
    });
}).catch( (err) => {
    console.error('Fetch error!');
    console.error(err);
});