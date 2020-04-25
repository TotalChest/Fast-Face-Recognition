#include <iostream>
#include <ctime>
#include <string>
#include <fstream>
#include <vector>
#include <sstream>
#include <algorithm>
#include <omp.h>
#include <map>

using namespace std;

const string vectors_file("../Vectors/Vectors.txt");
const string result_file("Results/Result_");
const string delimiter(",");
const int d = 128; //Размерность
const int q = 1000; // Количество запросов
int k_nearest = 50; // Количество ближайших соседей
const int K = 50; // Количество центроидов для каждого измерения
const int secondary_serach = 15; // Коэффициент объема вторичного поиска
const int threads = 8;

double dist(vector<double> &a, vector<double> &b)
{
	double dist = 0.0;
	for(int i = 0; i < d; ++i)
		dist += (a[i] - b[i]) * (a[i] - b[i]);
	return dist;
}

double dist_1(vector<double> &a, vector<double> &b)
{
	double dist = 0.0;
	for(int i = 0; i < d/2; ++i)
		dist += (a[i] - b[i]) * (a[i] - b[i]);
	return dist;
}

double dist_2(vector<double> &a, vector<double> &b)
{
	double dist = 0.0;
	for(int i = 0; i < d/2; ++i)
		dist += (a[i+d/2] - b[i]) * (a[i+d/2] - b[i]);
	return dist;
}

struct bhnode {
    double priority;
    int i;
    int j;
    bhnode(int i = 0, int j = 0, double priority = 1000): i(i), j(j), priority(priority) {}
};

class priority_queue {
public:
    priority_queue(int MAX) {
        body = new bhnode[maxsize = MAX+1];
        numnodes = 0;
    }   

    ~priority_queue() {
        delete [] body;
    }

    int insert(bhnode const &node) {
        if (numnodes > maxsize)
            return -1;
        body[++numnodes] = node;
        for (int i = numnodes; i > 1 && body[i].priority < body[i/2].priority; i /= 2) 
            swap(i, i/2);
        return 0; 
    }  

    bhnode *fetchMin() {
        return numnodes == 0? NULL : body + 1;
    }

    int removeMin() {
        if (numnodes == 0) return -1;
        body[1] = body[numnodes--];
        heapify(1);
        return 0;
    }
private:
    void heapify(int index) {
        for (;;) {
            int left = index + index; int right = left + 1;
            int largest = index;
            if (left <= numnodes && body[left].priority < body[index].priority)
                largest = left;
            if (right <= numnodes && body[right].priority < body[largest].priority)
                largest = right;
            if (largest == index) break;
            swap(index, largest);
            index = largest;
        }
    }

    void swap(int n1, int n2) {
        bhnode t = body[n1];
        body[n1] = body[n2];
        body[n2] = t;
    }
    bhnode *body;
    int numnodes;
    int maxsize;
};

int main(int argc, char **argv)
{
    if (argc > 2)
    {
        cout << "Usage: ./MultiIndexSearch <k_nearest>\n";
        return 0;
    }
    if (argc == 2)
        k_nearest = atoi(argv[1]);
    omp_set_num_threads(threads);
	ifstream file(vectors_file);
	string str;
  	vector< pair< string, vector<double> > > vectors;
  	vector< pair< string, vector<double> > > queries(q);
 	size_t count = 0;

  	while ((getline(file, str)))
  	{
		size_t pos = 0;
		pos = str.find(delimiter);
		vectors.push_back({str.substr(0, pos), vector<double>()});
		str.erase(0, pos + delimiter.length());

		while ((pos = str.find(delimiter)) != string::npos)
		{
    		vectors[count].second.push_back(stod(str.substr(0, pos)));
   			str.erase(0, pos + delimiter.length());
		}
		vectors[count].second.push_back(stod(str));
		++count;
  	}

  	srand(unsigned(time(0)));
  	for(int i = 0; i < q; ++i)
  	{
    	int index = rand() % count;
    	queries[i] = vectors[index];
    }

    cout << "START LEARNING...\n";

    vector< vector<double> > centroids_1(K); // Вектор центроидов первого измерения
    vector< vector<double> > centroids_2(K); // Вектор центроидов второго измерения
    vector<int> member_1(count, 0); // Вектор меток первого измерения
    vector<int> member_2(count, 0); // Вектор меток второго измерения

    for(int i = 0; i < K; ++i)
    {
        int index = rand() % count;
        for(int j = 0; j < d/2; ++j)
        	centroids_1[i].push_back(vectors[index].second[j]);
    }

    for(int i = 0; i < K; ++i)
    {
        int index = rand() % count;
        for(int j = 64; j < d; ++j)
        	centroids_2[i].push_back(vectors[index].second[j]);
    }

    cout << "FIRST CLUSTER...\n";

    for(int t = 0; t < 40; ++t)
    {   
        cout << "\r" << t << "/40" << flush;
        #pragma omp parallel for
        for(int i = 0; i < count; ++i)
        {
            double min = dist_1(vectors[i].second, centroids_1[0]);
            int cl = 0;
            for(int j = 1; j < K; ++j)
            {
                double distance = dist_1(vectors[i].second, centroids_1[j]);
                if(distance < min)
                {
                    min = distance;
                    cl = j;
                }
            }

            member_1[i] = cl;

        }

        #pragma omp parallel for
        for(int j = 0; j < K; ++j)
        {
            int num = 0;
            vector<double> temp(d/2,0);
            for(int i = 0; i < count; ++i)
                if(member_1[i] == j)
                {
                    ++num;
                    for(int g = 0; g < d/2; ++g)
                        temp[g] = temp[g] + vectors[i].second[g];
                }
            for(int i = 0; i < d/2; ++i)
                temp[i] /= num;
            centroids_1[j] = temp;
        }
    }
    cout << "\r" << "40/40" << endl;

    cout << "SECOND CLUSTER...\n";

    for(int t = 0; t < 40; ++t)
    {    
        cout << "\r" << t << "/40" << flush;
        #pragma omp parallel for
        for(int i = 0; i < count; ++i)
        {
            double min = dist_2(vectors[i].second, centroids_2[0]);
            int cl = 0;
            for(int j = 1; j < K; ++j)
            {
                double distance = dist_2(vectors[i].second, centroids_2[j]);
                if(distance < min)
                {
                    min = distance;
                    cl = j;
                }
            }

            member_2[i] = cl;

        }

        #pragma omp parallel for
        for(int j = 0; j < K; ++j)
        {
            int num = 0;
            vector<double> temp(d/2,0);
            for(int i = 0; i < count; ++i)
                if(member_2[i] == j)
                {
                    ++num;
                    for(int g = 0; g < d/2; ++g)
                        temp[g] = temp[g] + vectors[i].second[g+d/2];
                }
            for(int i = 0; i < d/2; ++i)
                temp[i] /= num;
            centroids_2[j] = temp;
        }
    }
    cout << "\r" << "40/40" << endl;

    cout << "START BUILD MULTIINDEX...\n";

    vector< vector < pair< string, vector<double> > > > MultiIndex(K*K);
    for(int i = 0; i < count; ++i)
    {
        double min_1 = dist_1(vectors[i].second, centroids_1[0]);
        double min_2 = dist_2(vectors[i].second, centroids_2[0]);
        int cl_1 = 0;
        int cl_2 = 0;
        #pragma omp parallel for
        for(int j = 1; j < K; ++j)
        {
            double distance_1 = dist_1(vectors[i].second, centroids_1[j]);
            double distance_2 = dist_2(vectors[i].second, centroids_2[j]);
            if(distance_1 < min_1)
            {
                min_1 = distance_1;
                cl_1 = j;
            }
            if(distance_2 < min_2)
            {
                min_2 = distance_2;
                cl_2 = j;
            }
        }
        
        MultiIndex[cl_1*K+cl_2].push_back({vectors[i].first, vectors[i].second});
    }

    vectors.clear();

    cout << "START SEARCHING...\n";
    ofstream res_file(result_file + to_string(k_nearest));
    res_file << "MultiIndexSearch k = " << k_nearest << "\nQueries: " << q << "\n";
    int total_true = 0;
    int face_true = 0;
    double total_time = 0;

    for(int i = 0; i < q; ++i)
  	{
    	vector< pair<double, int> > claster_dist_1(K);
    	vector< pair<double, int> > claster_dist_2(K);
    	vector< pair<double, string> > v_dist;

        clock_t start = clock();
        for(int j = 0; j < K; ++j)
        {
            claster_dist_1[j].second = j;
            claster_dist_1[j].first = dist_1(queries[i].second, centroids_1[j]);
            claster_dist_2[j].second = j;
            claster_dist_2[j].first = dist_2(queries[i].second, centroids_2[j]);
        }
        sort(claster_dist_1.begin(), claster_dist_1.end());
        sort(claster_dist_2.begin(), claster_dist_2.end());

        priority_queue PQueue(K*K);
        int total_count = 0;
        int iter_num = 0;
        int pq_size = 0;
        while(total_count < secondary_serach * k_nearest)
        {
        	if(pq_size == 0)
        	{
	        	for(int g = 0; g <= iter_num; ++g)
	        		PQueue.insert({claster_dist_1[g].second, claster_dist_2[iter_num-g].second, claster_dist_1[g].first + claster_dist_2[iter_num-g].first});
	        	++iter_num;
	        	pq_size = iter_num;
	        }

    		auto curr = PQueue.fetchMin();
    		PQueue.removeMin();
    		--pq_size;
    		for(auto elem: MultiIndex[K*curr->i + curr->j])
                v_dist.push_back({dist(queries[i].second, elem.second), elem.first});
    		total_count += MultiIndex[K*curr->i + curr->j].size();
        }
        sort(v_dist.begin(), v_dist.end());
    	clock_t end = clock();

    	cout << "Query: " << queries[i].first << endl;

    	int count_true = 0;
        map<string, int> freq;
    	for(int k = 1; k <= k_nearest; ++k)
    	{
    		string temp = v_dist[k].second;
            if (freq.find(temp.substr(0, 8)) == freq.end())
                freq[temp.substr(0, 8)] = 0;
            freq[temp.substr(0, 8)] +=1;
    		if(temp.substr(0, 8) == queries[i].first.substr(0, 8))
    		{
    			count_true++;
    		    cout << "###  " << temp << "   " << v_dist[k].first << endl;
    		}
    		else
    			cout << "     " << temp << "   " << v_dist[k].first << endl;
    	}

        int max_freq = 0;
        string face;
        for (auto elem: freq)
            if(elem.second > max_freq) {
                max_freq = elem.second;
                face = elem.first;
            }
        if (face == queries[i].first.substr(0, 8))
            face_true++;

    	total_true += count_true;
        total_time += ((end - start) / (double)CLOCKS_PER_SEC);
   		cout << "Searching time: " << ((end - start) / (double)CLOCKS_PER_SEC) << " seconds in " << count << " faces.\n" << endl;
    }

    res_file << "Search accuracy: " << 1.0*total_true/(q*k_nearest) << "\n";
    res_file << "Recognition accuracy: " << 1.0*face_true/q << "\n";
    res_file << "Time: " << total_time/q << "\n";
    res_file.close();
    file.close();

	return 0;
}