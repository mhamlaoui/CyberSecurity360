<<<<<<< HEAD
// Navigation 
document.querySelectorAll('.nav-item').forEach(item => {
    item.addEventListener('click', () => {
      document.querySelectorAll('.nav-item').forEach(navItem => {
        navItem.classList.remove('active');
      });
      item.classList.add('active');
    });
=======
// Navigation 
document.querySelectorAll('.nav-item').forEach(item => {
    item.addEventListener('click', () => {
      document.querySelectorAll('.nav-item').forEach(navItem => {
        navItem.classList.remove('active');
      });
      item.classList.add('active');
    });
>>>>>>> 05238f3a83981a3c4a40aa1103d176ca2d031b9c
  });