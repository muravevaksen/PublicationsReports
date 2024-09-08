  const ctx = document.getElementById('myChart').getContext('2d');
  const myChart = new Chart(ctx, {
      type: 'bar',
      data: {
        labels : [{% for a in authors %}"{{ a.name }}",{% endfor %}],
          datasets: [{
            label: "лабел",
            data : [{% for p in pcount %}{{ p }},{% endfor %}],
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 1
          }]
      },
      options: {
          scales: {
              y: {
                  beginAtZero: true
              }
          }
      }
  });