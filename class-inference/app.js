const fs = require('fs');
const CsvReadableStream = require('csv-reader');

class Distribution {
    constructor(data={}) { this.data = data }
    insert(x) {
        if (Object.keys(this.data).includes(x))
            this.data[x]++;
        else
            this.data[x] = 1;
    }
    mostFrequent() {
        return Object.entries(this.data).sort((a, b) => b[1]-a[1])[0];
    }
};

const parseRow = row => ({ s: row[0], p: row[1], o: row[2] });

const list_properties_per_subject = async file_name => {
    const properties_per_subject_file = `./properties_per_subject/${file_name}.json`;
    try {
        return require(properties_per_subject_file); 
    } catch(e) {}
    const file = `./data/${file_name}.csv`;
    return new Promise(resolve => {
        const seen = {};
        const inputStream = fs.createReadStream(file, 'utf8');
        const pipe = inputStream.pipe(new CsvReadableStream({ skipHeader: true }))
        pipe.on('data', row => {
            const { s, p, o } = parseRow(row); 
            if (!seen[s]) {
                seen[s] = [ p ];
            } else {
                if (!seen[s].includes(p)) {
                    seen[s].push(p);
                }
            }
        });
        pipe.on('end', () => {
            fs.writeFileSync(properties_per_subject_file, JSON.stringify(seen));
            resolve(seen);
        });
    });
}; 

const list_subjects_per_property = async file_name => {
    const subjects_per_property_file = `./subjects_per_property/${file_name}.json`;
    try {
        return require(subjects_per_property_file); 
    } catch(e) {}
    const file = `./data/${file_name}.csv`;
    return new Promise(resolve => {
        const seen = {};
        const inputStream = fs.createReadStream(file, 'utf8');
        const pipe = inputStream.pipe(new CsvReadableStream({ skipHeader: true }))
        pipe.on('data', row => {
            const { s, p, o} = parseRow(row); 
            if (!seen[p]) {
                seen[p] = [ s ];
            } else {
                if (!seen[p].includes(s)) {
                    seen[p].push(s);
                }
            }
        });
        pipe.on('end', () => {
            fs.writeFileSync(subjects_per_property_file, JSON.stringify(seen));
            resolve(seen);
        });
    });
};

let node_counter = 1;

class Node {
    constructor(properties_per_subject, subjects_per_property) {
        /* acts as id for a node */
        this.node_counter = node_counter++;
        /* all subjects in this node */
        this.subjects = Object.keys(properties_per_subject);
        /* all properties in this node */
        this.properties = Object.keys(subjects_per_property);
        /* maps subjects to a list of the properties it uses */
        this.properties_per_subject = properties_per_subject;
        /* maps properties to a list of the subjects it is used by */
        this.subjects_per_property = subjects_per_property;
        /* most used property of this node */
        this.most_used_property = this.mostUsedProperty();
        /* left branch - contains all instances that use the most used property */
        this.left = null;
        /* right branch - contains all instances that do not use the most used property */
        this.right = null;
        /* we can only branch if there are any subjects left */
        if (this.subjects.length) {
            this.branch();
        }
    }
    mostUsedProperty() {
        const propertyDistribution = new Distribution(); 
        for (const properties of Object.values(this.properties_per_subject)) {
            for (const p of properties) {
                propertyDistribution.insert(p);
            }
        }
        return propertyDistribution.mostFrequent(); 
    }
    branch() {
        const subjects = this.subjects_per_property[this.most_used_property[0]];
        const subjects_complement = this.subjects.filter(s => !subjects.includes(s));

        /* left branch - instances using most used properties */
        const properties_per_subject = {};
        const subjects_per_property = {};
        for (const subject of subjects) {
            const properties = this.properties_per_subject[subject].filter(p => p !== this.most_used_property[0]);
            if (properties.length) {
                properties_per_subject[subject] = properties; 
                for (const property of properties) {
                    if (!subjects_per_property[property]) {
                        subjects_per_property[property] = [subject];
                    } else {
                        subjects_per_property[property].push(subject);
                    }
                }
            }
        }
        this.left = new Node(properties_per_subject, subjects_per_property);

        /* right branch - complement of instances using most used properties */
        const complement_properties_per_subject = {};
        const complement_subjects_per_property = {};
        for (const subject of subjects_complement) {
            const properties = this.properties_per_subject[subject];
            complement_properties_per_subject[subject] = properties;
            if (properties.length) {
                for (const property of properties) {
                    if (!complement_subjects_per_property[property]) {
                        complement_subjects_per_property[property] = [subject];
                    } else {
                        complement_subjects_per_property[property].push(subject);
                    }
                }
            }
        }
        this.right = new Node(complement_properties_per_subject, complement_subjects_per_property);
    }
    print() {
        if (this.node_counter && this.subjects) {
            console.log(`${this.node_counter} ;`);
            console.log(`${this.node_counter} [label="{${this.subjects.length}}"];`);
        }
        if (this.left && this.left.node_counter && this.most_used_property) {
            console.log(`${this.node_counter} -> ${this.left.node_counter} [label="${this.most_used_property[0]}"];`);
            this.left.print();
        }
        if (this.right && this.right.node_counter) {
            console.log(`${this.node_counter} -> ${this.right.node_counter} [label="complement"];`);
            this.right.print();
        }
    }
    serialize(file_name) {
        const serialization = JSON.stringify({
            node_counter: this.node_counter,
            subjects: this.subjects,
            properties: this.properties,
            properties_per_subject: this.properties_per_subject,
            subjects_per_property: this.subjects_per_property,
            most_used_property: this.most_used_property,
            left: this.left,
            right: this.right,
        });
        fs.writeFileSync(`./property_usage_hierarchy/${file_name}.json`, serialization);
    }

    static innerDeserialize(serialization) {
        if (!serialization)
            return null;
        let node = new Node({}, {});
        node.node_counter = serialization.node_counter;
        node.subjects = serialization.subjects;
        node.properties = serialization.properties;
        node.properties_per_subject = serialization.properties_per_subject;
        node.subjects_per_property = serialization.subjects_per_property;
        node.most_used_property = serialization.most_used_property;
        node.left = Node.innerDeserialize(serialization.left);
        node.right = Node.innerDeserialize(serialization.right);
        return node;
    }

    static deserialize(file_name) {
        const serialization = require(`./property_usage_hierarchy/${file_name}.json`);
        let node = new Node({}, {});
        node.node_counter = serialization.node_counter;
        node.subjects = serialization.subjects;
        node.properties = serialization.properties;
        node.properties_per_subject = serialization.properties_per_subject;
        node.subjects_per_property = serialization.subjects_per_property;
        node.most_used_property = serialization.most_used_property;
        node.left = Node.innerDeserialize(serialization.left);
        node.right = Node.innerDeserialize(serialization.right);
        return node;
    }
};

/* MAIN */
(async _ => {
    const file_name = process.argv[2];

    /* creatse a list of properties used for every subject */
    const properties_per_subject = await list_properties_per_subject(file_name);
    /* create a list of properties used for every subject */
    const subjects_per_property = await list_subjects_per_property(file_name);

    /* create or read pre-existing root node of anonymous class hierarchy */
    let hierarchy = null;
    try {
        hierarchy = Node.deserialize(file_name); 
    } catch(e) {
        hierarchy = new Node(properties_per_subject, subjects_per_property); 
        hierarchy.serialize(file_name);
    }

    /* print hierarchy in .viz format */
    console.log('digraph {');
    hierarchy.print();
    console.log('}');
})();
