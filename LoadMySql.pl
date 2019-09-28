#!/usr/bin/perl

# DBI is the standard database interface for Perl
# DBD is the Perl module that we use to connect to the MySQL database
use DBI;
use DBD::mysql;
use warnings;

$database = "weather";

#----------------------------------------------------------------------
# open the data file
#----------------------------------------------------------------------

my $file = $ARGV[0] or die "Need to get CSV file on the command line\n";

#----------------------------------------------------------------------
# insert the values into the database
#----------------------------------------------------------------------

# invoke the ConnectToMySQL sub-routine to make the database connection
$connection = ConnectToMySql($database) or die "Unable to connect to MySQL\n";

open(my $data, '<', $file) or die "Could not open '$file' $!\n";
my $count=0;

while (my $line = <$data>) {
  chomp $line;
 
  my @f = split "," , $line;
  # set the value of your SQL query
  # then prepare your statement for connecting to the database
  
  #print "$f[0] $f[8] $f[9]\n";
  $query = "delete from calib where indx=?";
  $statement = $connection->prepare($query);
  $statement->execute($f[0]);
  $query = "insert into calib (indx, intvl, int_hum, int_temp, ext_hum, ext_temp, abs_press, 
			rel_press, wind, gust, wind_dir, rain, status) 
			values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)";
  $statement = $connection->prepare($query);
  $statement->execute($f[0],$f[1],$f[2],$f[3],$f[4],$f[5],$f[6],$f[7],$f[8],$f[9],$f[10],$f[11],$f[12]);
  $count++;
}
print "Processed $count rows for $file\n";

#----------------------------------------------------------------------


#----------------------------------------------------------------------
# retrieve the values from the database
#----------------------------------------------------------------------

# set the value of your SQL query
#$query2 = "select indx, wind, gust from calib";

# prepare your statement for connecting to the database
#$statement = $connection->prepare($query2);

# execute your SQL statement
#$statement->execute();

# we will loop through the returned results that are in the @data array
# even though, for this example, we will only be returning one row of data

#   while (@data = $statement->fetchrow_array()) {
#      $name_first = $data[0];
#      $name_last = $data[1];
#      $address_01 = $data[2];
#
#print "RESULTS - $name_first, $name_last, $address_01\n";

#}

#----------------------------------------------------------------------


# exit the script
exit;

#--- start sub-routine ------------------------------------------------
sub ConnectToMySql {
#----------------------------------------------------------------------

my ($db) = @_;

# open the accessDB file to retrieve the database name, host name, user name and password
#open(ACCESS_INFO, "<..\/accessAdd") || die "Can't access login credentials";

# assign the values in the accessDB file to the variables
my $database = 'weather';
my $host = 'thelinux';
my $userid = 'weather_rw';
my $passwd = 'Weather123Za';

# assign the values to your connection variable
my $connectionInfo="dbi:mysql:database=$db;host=$host";

# close the accessDB file
#close(ACCESS_INFO);

# the chomp() function will remove any newline character from the end of a string
chomp ($database, $host, $userid, $passwd);

# make connection to database
my $l_connection = DBI->connect($connectionInfo,$userid,$passwd);

# the value of this connection is returned by the sub-routine
return $l_connection;

}
