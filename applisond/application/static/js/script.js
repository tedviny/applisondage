// Effet de visibilité avec transition
const ratio = .1;
const options = {
    root: null,
    rootMargin: '0px',
    threshold: ratio
  }

const handleIntersect = function(entries, observer){
   entries.forEach(function(entry) {
       if(entry.intersectionRatio > 0){
           entry.target.classList.add('reveal-visible')
           console.log('visible')
       }
   })
}
  
const observer = new IntersectionObserver(handleIntersect, options);
document.querySelectorAll('.reveal').forEach(function (r) {
observer.observe(r)

})




  