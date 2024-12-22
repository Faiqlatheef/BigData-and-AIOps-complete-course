import java.io.IOException;
import java.util.StringTokenizer;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
//Removed URL for Hadoop API documentation
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class MovieRatingCount {

  public static class MovieRatingMapper extends Mapper<LongWritable, Text, Text, IntWritable> {

    private final Text rating = new Text();
    private final IntWritable one = new IntWritable(1);

    @Override
    public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
      // Tokenize the line based on tab separation
      StringTokenizer itr = new StringTokenizer(value.toString(), "\t");

      // Skip header line (if present)
      if (itr.hasMoreTokens() && key.compareTo(new LongWritable(0)) != 0) {
        // Extract rating
        itr.nextToken(); // Skip user ID
        itr.nextToken(); // Skip movie ID
        rating.set(itr.nextToken());

        // Emit key-value pair (rating, 1)
        context.write(rating, one);
      }
    }
  }

  public static class MovieRatingReducer extends Reducer<Text, IntWritable, Text, IntWritable> {

    private final IntWritable count = new IntWritable();

    @Override
    public void reduce(Text key, Iterable<IntWritable> values, Context context)
        throws IOException, InterruptedException {
      int sum = 0;
      for (IntWritable val : values) {
        sum += val.get();
      }
      count.set(sum);

      // Emit key-value pair (rating, total count)
      context.write(key, count);
    }
  }

  public static void main(String[] args) throws Exception {
    Configuration conf = new Configuration();

    // Replace with path to u.data file on HDFS
    Path inputPath = new Path("/u.data");
    Path outputPath = new Path("/output/movie_rating_count");

    Job job = Job.getInstance(conf, "MovieRatingCount");
    job.setJarByClass(MovieRatingCount.class);
    job.setMapperClass(MovieRatingMapper.class);
    job.setCombinerClass(MovieRatingReducer.class); // Optional: Improve efficiency
    job.setReducerClass(MovieRatingReducer.class);
    job.setOutputKeyClass(Text.class);
    job.setOutputValueClass(IntWritable.class);

    FileInputFormat.addInputPath(job, inputPath);
    FileOutputFormat.setOutputPath(job, outputPath);

    System.exit(job.waitForCompletion(true) ? 0 : 1);
  }
}
