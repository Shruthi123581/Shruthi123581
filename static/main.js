function displayTasks(projectId) {
    // Make an AJAX request to fetch the tasks for the selected project
    $.ajax({
      url: '/get_tasks/',
      type: 'GET',
      data: {
        project_id: projectId
      },
      success: function(response) {
        // Process the response and display the tasks
        // You can update the DOM to show the tasks in a modal, another section of the page, etc.
        console.log(response);
      },
      error: function(error) {
        console.log(error);
      }
    });
  }
