module.exports = function(grunt) {

  // Project configuration.
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    uglify: {
      options: {
        banner: '/*! <%= pkg.name %> <%= grunt.template.today("yyyy-mm-dd") %> */\n'
      },
      build: {
        src: 'src/<%= pkg.name %>.js',
        dest: 'salvius/static/js/<%= pkg.name %>.min.js'
      }
    }
  });

  // Load tasks
  grunt.loadNpmTasks('grunt-contrib-uglify');

  // Register tasks
  grunt.registerTask('default', ['uglify']);
  grunt.registerTask('default', 'Example custom task.', function() {
    grunt.log.write('An example custom task.').ok();
  });


};
