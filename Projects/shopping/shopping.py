import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])

    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")

def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    evidence = []
    labels = []
    month = ["jan", "feb", "mar", "apr", "may", "june", "jul", "aug", "sep", "oct", "nov", "dec"]

    with open(filename) as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            if row.pop("Revenue").lower() == "true":
                labels.append(1)
            else:
                labels.append(0)

            templist = list(row.values())
            templist[0] = int(templist[0])
            templist[1] = float(templist[1])
            templist[2] = int(templist[2])
            templist[3] = float(templist[3])
            templist[4] = int(templist[4])
            templist[5] = float(templist[5])
            for temp in templist[6:10]:
                templist[templist.index(temp)] = float(temp)
            templist[10] = month.index(templist[10].lower())
            for temp in templist[11:15]:
                templist[templist.index(temp)] = int(temp)
            if templist[15].lower() == "returning_visitor":
                templist[15] = 1
            else:
                templist[15] = 0
            if templist[16].lower() == "true":
                templist[16] = 1
            else:
                templist[16] = 0

            evidence.append(templist)

    return (evidence, labels)


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence, labels)
    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    sen = 0
    sensitivity = 0
    spe = 0
    specificity = 0

    for lab, pred in zip(labels, predictions):
        if lab == 1:
            sen += 1
            if pred == 1: sensitivity += 1
        if lab == 0:
            spe += 1 
            if pred == 0: specificity += 1

    return (sensitivity/sen, specificity/spe)


if __name__ == "__main__":
    main()
