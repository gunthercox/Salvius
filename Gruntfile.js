module.exports = function(grunt) {

var path = require('path');

  // Project configuration.
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),

    uglify: {
      options: {
        mangle: true,
        preserveComments: false
      },
      assets: {
        files: {
          'salvius/static/js/assets.min.js': [
            'bower_components/jquery/dist/jquery.js',
            'bower_components/bootstrap-sass/assets/javascripts/bootstrap.js',
            'bower_components/chartist/dist/chartist.js',
            'bower_components/jquery-knob/js/jquery.knob.js',
            'bower_components/jquery-network-camera/jquery.network-camera.js',
            'bower_components/jquery-throttle-debounce/jquery.ba-throttle-debounce.js',
            'bower_components/moment/moment.js',
            'bower_components/virtualjoystick.js/virtualjoystick.js'
          ]
        }
      },
      robot: {
        files: {
          'salvius/static/js/robot.min.js': [
            'salvius/static/js/robot.js',
            'salvius/static/js/robot.torso.js',
            'salvius/static/js/robot.status.js',
            'salvius/static/js/robot.events.js',
          ]
        }
      }
    },

    sass: {
      dist: {
        files: {
          'salvius/static/css/assets.min.css': 'salvius/static/css/assets.sass'
        }
      }
    },

    copy: {
      fonts: {
        files: [
          {
            cwd: 'bower_components/font-awesome/fonts/',
            src: '*',
            dest: 'salvius/static/fonts/',
            expand: true,
            filter: 'isFile'
          }
        ]
      }
    }


  });

  // Load tasks
  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-sass');
  grunt.loadNpmTasks('grunt-contrib-copy');

  grunt.registerTask('default', [
    'uglify:assets',
    'uglify:robot',
    'sass',
    'copy:fonts'
  ]);

};
