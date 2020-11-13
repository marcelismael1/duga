
			// let ctx = document.getElementById('myChart').getContext('2d');
			new Chart(document.getElementById("SOFAlarms"),
				{
					"type":"doughnut",
					"data":{
						"labels":["Low","Meduim","High","Critical"],
						"datasets":[{
							"label":"My First Dataset",
							"data": {{ SOFAlarms }} ,
								// [300,
								// 50,
								// 100,
								// 200],
							"backgroundColor":[
								"rgb(33, 213, 155)",
								"rgb(0, 88, 255)",
								"rgb(255, 199, 0)",
								"rgb(249, 0, 0)",
								]
				}
				]
			}
		});

		

				
			// let ctx = document.getElementById('myChart').getContext('2d');
			new Chart(document.getElementById("Totalseverity"),
				{
					"type":"doughnut",
					"data":{
						"labels":["Low","Meduim","High","Critical"],
						"datasets":[{
							"label":"My First Dataset",
							"data": {{ Totalseverity }} ,
								// [300,
								// 50,
								// 100,
								// 200],
							"backgroundColor":[
								"rgb(33, 213, 155)",
								"rgb(0, 88, 255)",
								"rgb(255, 199, 0)",
								"rgb(249, 0, 0)",
								]
				}
				]
			}
		});

		

		
			var monthlyData = {
			   labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'] ,
			   datasets: [{
			      label: "Low",
			      barThickness: 10,
			      backgroundColor: "rgb(33, 213, 155)",
			      data: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
			   }, {
			      label: "Critical",
			      barThickness: 12,
			      backgroundColor: "rgb(249, 0, 0)",
			      data: [12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
			   }]
			};

			var malarm = document.getElementById('Monthlyalarm');
			var myBarChart = new Chart(malarm, {
			   type: "bar",
			   data: monthlyData,
			   options: {
			      scales: {
			         yAxes: [{
			            display: true,

			            ticks: {
			               min: 0,
			               max: 50
			            }
			         }]
			      }
			   }
			});
	